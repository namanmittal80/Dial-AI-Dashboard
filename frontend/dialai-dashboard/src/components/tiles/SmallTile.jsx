import React from 'react';
import '../../styles/Tiles.css';

const SmallTile = ({ title, value, icon, layout = "default" }) => {
  if (layout === "modern") {
    return (
      <div className="small-tile tile transition-all hover:shadow-md">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>{title}</h3>
          <div className="tile-icon">{icon}</div>
        </div>
        <div className="mt-3">
          <p className="tile-value">{value}</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="small-tile tile">
      <div className="tile-icon">{icon}</div>
      <div className="tile-content">
        <h3 className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>{title}</h3>
        <p className="tile-value">{value}</p>
      </div>
    </div>
  );
};

export default SmallTile; 