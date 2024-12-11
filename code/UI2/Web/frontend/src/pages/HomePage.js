import React from 'react';
import Header from '../components/Header';
import ImageUpload from '../components/ImageUpload';
import ImageList from '../components/ImageList';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-container">
      <Header />
      <ImageUpload />
      <ImageList />
    </div>
  );
};

export default HomePage;
