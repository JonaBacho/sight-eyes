import os
import cv2
import math
import time
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util, visualization_utils as vis_util
from utils.app_utils import FPS, WebcamVideoStream, HLSVideoStream, sign
from utils.stream import ESP32VideoStream
from threading import Event


class ObjectTracker:
    def __init__(self, source='webcam', stream_url=None, image_path=None, target_name=None, fov_horizontal=60, fov_vertical=40, webcam_width=640, webcam_height=480):
        """
        Initialise le tracker d'objets.

        :param source: 'webcam' ou 'stream' ou 'video' pour choisir la source vidéo.
        :param stream_url: URL du flux vidéo en streaming (requis si source='stream').
        :param image_path: Chemin vers une image pour identifier l'objet cible.
        :param target_name: Nom de l'objet cible parmi les 90 reconnus.
        :param fov_horizontal: Champ de vision horizontal en degrés (par défaut 60 pour ESP32-cam).
        :param fov_vertical: Champ de vision vertical en degrés (par défaut 40 pour ESP32-cam).
        :param webcam_width: Largeur de la vidéo pour webcam (par défaut 640 pixels).
        :param webcam_height: Hauteur de la vidéo pour webcam (par défaut 480 pixels).
        :param port_arduino: Chemin du port série pour communiquer avec Arduino (par défaut '/dev/ttyUSB0').
        """
        self.source = source
        self.stream_url = stream_url
        self.image_path = image_path
        self.target_name = target_name
        self.fov_horizontal = fov_horizontal
        self.fov_vertical = fov_vertical
        self.webcam_width = webcam_width
        self.webcam_height = webcam_height

        self.model_name = 'ssd_mobilenet_v1_coco_11_06_2017'
        self.cwd_path = os.getcwd()
        self.path_to_ckpt = os.path.join(self.cwd_path, 'object_detection', self.model_name, 'frozen_inference_graph.pb')
        self.path_to_labels = os.path.join(self.cwd_path, 'object_detection', 'data', 'mscoco_label_map.pbtxt')
        self.num_classes = 90
        self.category_index = self._load_label_map()
        self.detection_graph, self.sess = self._load_model()
        self.target_id = None
        self.servo_horizontal_angle = 90  # Angle initial du servo horizontal
        self.servo_vertical_angle = 90  # Angle initial du servo vertical
        self.max_angle = 180
        self.min_angle = 0
        self.max_screen_ratio = 0.8  # 80% de la taille de l'écran
        self.current_speed = 0  # Vitesse initiale
        self.object_found = False
        #self.arduino_comm = ArduinoCommunication(port=port_arduino, baudrate=9600)
        self.stop_event = Event()

        # Identifie l'objet cible
        try:
            if self.image_path:
                self.target_id = self._identify_target_from_image()
            elif self.target_name:
                self.target_id = self._get_target_id_by_name()
        except Exception as e:
            print(f"Erreur lors de l'identification de l'objet cible : {e}")

    def reset_event(self):
        self.stop_event = Event()

    def _load_label_map(self):
        label_map = label_map_util.load_labelmap(self.path_to_labels)
        categories = label_map_util.convert_label_map_to_categories(
            label_map, max_num_classes=self.num_classes, use_display_name=True
        )
        return label_map_util.create_category_index(categories)

    def _load_model(self):
        try:
            detection_graph = tf.compat.v1.Graph()
            with detection_graph.as_default():
                od_graph_def = tf.compat.v1.GraphDef()
                with tf.io.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                    serialized_graph = fid.read()
                    od_graph_def.ParseFromString(serialized_graph)
                    tf.compat.v1.import_graph_def(od_graph_def, name='')
            sess = tf.compat.v1.Session(graph=detection_graph)
            return detection_graph, sess
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement du modèle : {e}")

    def _identify_target_from_image(self):
        """Identifie l'objet cible à partir d'une image donnée."""
        try:
            image = cv2.imread(self.image_path)
            image_np_expanded = np.expand_dims(image, axis=0)
            image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

            (boxes, scores, classes, num_detections) = self.sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded}
            )

            # Retourner l'ID de l'objet avec le score le plus élevé
            target_id = np.squeeze(classes).astype(np.int32)[0]
            return target_id
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'identification à partir de l'image : {e}")

    def _get_target_id_by_name(self):
        """Retourne l'ID de l'objet en fonction de son nom."""
        for category_id, category_info in self.category_index.items():
            if category_info['name'] == self.target_name:
                return category_id
        raise ValueError(f"L'objet '{self.target_name}' n'est pas reconnu par le modèle.")

    def _calculate_servo_angles(self, box, frame_width, frame_height):
        """Calcule les angles pour ajuster les servos."""
        ymin, xmin, ymax, xmax = box
        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2
        print(f"x_center: {x_center}, y_center: {y_center}")
        sign_horizontal = sign(x_center - (frame_width / 2))
        sign_vertical = sign(y_center - (frame_height / 2))

        coeff_horizontal = 2 * sign_horizontal * abs(x_center - (frame_width / 2)) * math.tan(math.radians((sign_horizontal * self.fov_horizontal/2) + 90)) / frame_width
        new_servo_horizontal_angle = (self.servo_horizontal_angle + math.degrees(math.atan(coeff_horizontal))) % 360

        coeff_vertical = 2 * sign_vertical * abs(y_center - (frame_height / 2)) * math.tan(math.radians((sign_vertical * self.fov_vertical/2) + 90)) / frame_height
        new_servo_vertical_angle = (self.servo_vertical_angle + math.degrees(math.atan(coeff_vertical))) % 360
        print(f"new_servo_horizontal_angle: {new_servo_horizontal_angle}, new_servo_vertical_angle: {new_servo_vertical_angle}")

        self.servo_horizontal_angle = new_servo_horizontal_angle
        self.servo_vertical_angle = new_servo_vertical_angle
        #self.servo_horizontal_angle = max(self.min_angle, min(self.max_angle, new_servo_horizontal_angle))
        #self.servo_vertical_angle = max(self.min_angle, min(self.max_angle, new_servo_vertical_angle))

        return self.servo_horizontal_angle, self.servo_vertical_angle

    def _calculate_speed(self, box, frame_width, frame_height):
        # Calcul de la taille de l'objet par rapport à l'écran
        ymin, xmin, ymax, xmax = box
        obj_width = xmax - xmin
        obj_height = ymax - ymin
        obj_area_ratio = obj_width * obj_height

        # Vitesse décroissante
        if obj_area_ratio >= self.max_screen_ratio:
            return 0  # Arrêt du robot
        self.current_speed = max(0.1, 1 - obj_area_ratio)
        return self.current_speed  # Vitesse réduite en fonction de la taille

    def _process_frame(self, frame):
        found = False
        """Traite une seule image pour détecter et suivre l'objet cible."""
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_np_expanded = np.expand_dims(frame_rgb, axis=0)

            # Récupération des tenseurs
            image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

            # Exécution de l'inférence

            (boxes, scores, classes, num_detections) = self.sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded}
            )

            # Suivi de l'objet cible uniquement
            for i, class_id in enumerate(np.squeeze(classes).astype(np.int32)):
                if class_id == self.target_id and np.squeeze(scores)[i] > 0.5:
                    box = np.squeeze(boxes)[i]
                    found = True
                    frame_width, frame_height = frame.shape[1], frame.shape[0]
                    horizontal_angle, vertical_angle = self._calculate_servo_angles(box, frame_width, frame_height)
                    speed = self._calculate_speed(box, frame_width, frame_height)
                    is_close = True if speed == 0 else False
                    #self.arduino_comm.send_data(horizontal_angle, vertical_angle, speed, is_close)  # envoi à l'arduino
                    print(f"Angles: Horizontal={horizontal_angle:.2f}, Vertical={vertical_angle:.2f}")
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame, np.expand_dims(box, axis=0), np.array([class_id]), np.array([np.squeeze(scores)[i]]),
                        self.category_index, use_normalized_coordinates=True, line_thickness=8
                    )
                    break
            self.object_found = found
            return frame, found
        except Exception as e:
            print(f"Erreur lors du traitement de l'image : {e}")
            return frame, found

    def stop_tracking(self):
        self.stop_event.set()

    def start_tracking(self):
        """Démarre le suivi de l'objet à partir de la source vidéo."""
        try:
            if self.source == 'webcam':
                video_capture = WebcamVideoStream(src=0, width=self.webcam_width, height=self.webcam_height).start()
            elif self.source == 'stream' and self.stream_url:
                video_capture = ESP32VideoStream(url=self.stream_url).start()
            elif self.source == 'video':
                video_capture = HLSVideoStream(src=1).start()
            else:
                raise ValueError("Source vidéo non valide.")

            fps = FPS().start()
            while not self.stop_event.is_set():
                frame = video_capture.read()
                frame, found = self._process_frame(frame)

                if not found:
                    #self.arduino_comm.send_data(self.servo_horizontal_angle, self.servo_vertical_angle, 0, rotate=True)
                    print("Object not found")

                #distance = self.arduino_comm.receive_distance()
                distance = 100
                if distance and distance < 10:  # Ex. seuil pour l'arrêt
                    self.stop_event.set()
                    break

                cv2.imshow('Object Tracker', frame)
                fps.update()
                key = cv2.waitKey(1)
                if key == 27:   # correspond à ESC
                    break

            fps.stop()
            video_capture.stop()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"Erreur lors du suivi : {e}")

# Exemple d'utilisation
if __name__ == '__main__':
    tracker = ObjectTracker(source='stream', stream_url='http://172.20.10.8', target_name='person')
    #path = os.getcwd() + os.sep + 'media' + os.sep + 'cell_phone.jpeg'
    #tracker = ObjectTracker(source='webcam', image_path=path, target_name=None)
    #print(tracker.target_id)
    tracker.start_tracking()
