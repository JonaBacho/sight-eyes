import tensorflow as tf

# Chemin vers le modèle TensorFlow
model_path = 'object_detection/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb'

# Convertir en TensorFlow Lite
#converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
#tflite_model = converter.convert()

# Chemin vers le graphe figé
graph_def_file = "object_detection/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb"
input_arrays = ["image_tensor"]  # Remplacez par le nom exact de l'entrée du modèle
output_arrays = ["boxes", "scores", "classes", "num_detections"]  # Remplacez par vos sorties

converter = tf.lite.TFLiteConverter.from_frozen_graph(
    graph_def_file, input_arrays, output_arrays
)
tflite_model = converter.convert()

model_lite_path = 'object_detection/ssd_mobilenet_v1_coco_11_06_2017/lite_version/frozen_inference_graph_lite.pb'

# Sauvegarder le modèle converti
with open(model_lite_path, 'wb') as f:
    f.write(tflite_model)

print("Conversion réussie !")
