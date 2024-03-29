import ResultPage from "../../components/ResultPage/ResultPage";
import {useState, useEffect, useContext} from 'react';
import {useParams, useNavigate} from "react-router-dom";
import {CacheContext} from "../../context/CacheContext";
import OpenOogleLogo from '../../images/logo-ver2-removebg.png';
import axios from "axios";
import './Result.css';

const Results = () => {
    const backURL = process.env.REACT_APP_BACKEND_URL;
    const {query} = useParams();
    const [results, setResults] = useState([]);
    const [queryInputValue, setQueryInputValue] = useState(query);
    let navigate = useNavigate();
    // cache mechanism for query that we already request
    const { updateCache, getFromCache } = useContext(CacheContext);

    useEffect(() => {
      const fetchData = async () => {

          const cachedData = getFromCache(query);

          if (cachedData){
              // use results from cache
              setResults(cachedData);
          } else {
              try {
                  const response = await axios.get(`${backURL}/search?q=${query}`);
                  const data = JSON.parse(response.data);
                  setResults(data);
                  // save results in cache
                  updateCache(query, data);
              } catch (error) {
                  console.error(error);
              }
          }
      };
      fetchData();
    }, [query]);

    const search = () => {
        if (queryInputValue !== query){
            navigate('/search-results/'+queryInputValue);
            setResults([]);
        }
    }

    return (
        <div className='container'>

            <div className='search_bar_top'>
                <img src={OpenOogleLogo} alt="OpenOogle" onClick={() => navigate('/')}/>

                <div className="search_top">
                    <div className="searchbar-wrapper">
                        <div className="searchbar-left">
                            <div className="search-icon-wrapper" onClick={search}>
                <span className="search-icon searchbar-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path
                            d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z">
                        </path>
                    </svg>
                </span>
                            </div>
                        </div>

                        <div className="searchbar-center">
                            <div className="searchbar-input-spacer"></div>

                            <input type="text" className="searchbar-input"
                                   maxLength="2048"
                                   name="q"
                                   autoCapitalize="off"
                                   autoComplete="off"
                                   title="Search"
                                   role="combobox"
                                   placeholder="Search OpenOogle"
                                   aria-controls="dropdown-menu"
                                   aria-expanded={true}
                                   value={queryInputValue}
                                   onKeyUp={(e) => {
                                       if(e.key==='Enter'){
                                           search()
                                       }}
                                   }
                                   onChange={(e)=>setQueryInputValue(e.target.value)}
                            />
                        </div>
                    </div>
                </div>


            </div>

            {results.length > 0 ? results.map(res => <ResultPage key={res.rank} {...res} />)
                : (
                    <>
                        <div className="loader-container">
                            <div className="spinner"></div>
                        </div>
                        <div className='description'>
                                <h3>OpenOogle - ads free open source search system</h3>
                        </div>
                    </>
                )}
        </div>
    )
}

export default Results;