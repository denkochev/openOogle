import React, { createContext, useState, useEffect } from 'react';

const CacheContext = createContext();

const CacheProvider = ({ children }) => {
  const [cache, setCache] = useState(checkStorage);

  function checkStorage(){
    // Отримуємо значення з localStorage під час завантаження компонента
    const cachedData = JSON.parse(localStorage.getItem('cacheData'));
    if (cachedData) {
      return cachedData;
    } else {
      return {}
    }
  }

  useEffect(() => {
    // Зберігаємо значення в localStorage при зміні cache
    localStorage.setItem('cacheData', JSON.stringify(cache));
  }, [cache]);

  const updateCache = (query, data) => {
    setCache(prevCache => ({
      ...prevCache,
      [query]: data,
    }));
  };

  const getFromCache = (query) => {
    return cache[query] || null;
  };

  return (
    <CacheContext.Provider value={{ cache, updateCache, getFromCache }}>
      {children}
    </CacheContext.Provider>
  );
};

export { CacheContext, CacheProvider };
