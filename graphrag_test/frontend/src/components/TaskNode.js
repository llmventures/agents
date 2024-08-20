import React from 'react';
import { Handle, Position } from '@xyflow/react';

const TaskNode = ({data}) => {
    return (
        <div style={{
            padding: 10,
            border: '2px solid black',
            borderRadius: 5,
            backgroundColor: '#f0f0f0',
            width: '150px', // Optional: Set a fixed width
            position: 'relative' // Ensure handles are positioned correctly
          }}>
        <div>{data.label}</div>
        
        <div style={{ position: 'absolute', top: '50%', left: '-10px', transform: 'translateY(-50%)' }}>
        <Handle type="target" position="left" id="left-1" />
        <span style={{ position: 'absolute', left: '-50px' }}>Input</span>
        </div>
        
        <div style={{ position: 'absolute', top: '50%', right: '-10px', transform: 'translateY(-50%)' }}></div>
        <Handle type="target" position="right" id="right-1" />
        <span style={{ position: 'absolute', right: '-50px', top: '40px' }}>Input</span>
        
        <div style={{ position: 'absolute', top: '-10px', left: '50%', transform: 'translateX(-50%)' }}>
            <Handle type="target" position="top" id="top-1" />
            <span style={{ position: 'absolute', top: '-10px', left: '10px' }}>Input</span>
        </div>
        <div style={{ position: 'absolute', bottom: '-10px', left: '50%', transform: 'translateX(-50%)' }}>
        <Handle type="source" position="bottom" id="bottom-1" />
        <span style={{ position: 'absolute', bottom: '-10px', left: '10px' }}>Output</span>
          </div>
        </div>

    );
};

export default TaskNode;