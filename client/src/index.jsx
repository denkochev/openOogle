import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Main from './Pages/Main/Main';
import Results from './Pages/Results/Results';
import {CacheProvider} from './context/CacheContext';

import {
    createBrowserRouter,
    createRoutesFromElements,
    RouterProvider,
    Route,
    Outlet
} from 'react-router-dom';

const Root = () => {
    return (
        <div>
            <Outlet />
        </div>
    )
};

const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path='/' element={<Root />}>
            <Route index element={ <Main />} />
            <Route path='search-results/:query' element={ <Results />} />
        </Route>
    )
)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <CacheProvider>
        <RouterProvider router={router} />
    </CacheProvider>
);
