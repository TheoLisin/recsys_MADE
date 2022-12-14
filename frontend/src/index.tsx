import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { CacheProvider } from '@rest-hooks/react';

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);

const managers = [...CacheProvider.defaultProps.managers];

root.render(
    <CacheProvider managers={managers}>
        <React.StrictMode>
            <App />
        </React.StrictMode>
    </CacheProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
