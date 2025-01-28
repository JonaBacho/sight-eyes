import React, { useEffect, useState } from 'react';

const RecentSearches = () => {
    const [recentImages, setRecentImages] = useState([]);

    useEffect(() => {
        fetch('/upload/recent-searches')
            .then((res) => res.json())
            .then((data) => setRecentImages(data));
    }, []);

    return (
        <div>
            <h2>Objets récemment recherchés</h2>
            <ul>
                {recentImages.map((img) => (
                    <li key={img._id}>{img.objectName}</li>
                ))}
            </ul>
        </div>
    );
};

export default RecentSearches;
