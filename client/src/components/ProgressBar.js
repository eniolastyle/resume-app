import React from 'react';
import '../styles/progressbar.css';

const ProgressBar = ({ value }) => {
  return (
    <div className='progressBar'>
      <div className='progress' style={{ width: `${value}%` }}></div>
    </div>
  );
};

export default ProgressBar;
