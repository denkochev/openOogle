import {Rating} from '@mui/material';
import {useState} from 'react';
import axios from "axios";
import './ResultPage.css';

const ResultPage = ({rank, link, snippet, title, query}) => {
    const [evaluator, setEvaluator] = useState(false);
    const [evaluateStatus,setEvaluateStatus] = useState(false);
     const backURL = process.env.REACT_APP_BACKEND_URL;
    const evaluateResult = (userRating)=>{
        const userScore = userRating * 2;

        axios.post(backURL+'/evaluate', {
            query: query,
            link: link,
		    score: userScore
          })
          .then((response) => {
            if(response.data.success){
                // show 'Thanks text'
                setEvaluateStatus(true);
                // close Rating page
                setEvaluator(false);
            }
          })
          .catch((error)  =>{
            console.log(error);
          });
    }

    return (
        <div className='page-result'>
            {/*<p>{rank}</p>*/}
            <span className='pure-link'>{decodeURIComponent(link)}</span>
            <a href={link}>{title}</a>
            <p>{snippet}</p>
            {evaluator?
                <Rating defaultValue={0} precision={0.5} name={`result${rank}`}
                    onChange={(event, newValue) => {
                        evaluateResult(newValue);
                    }}
                />
                :
                    evaluateStatus? <span className='thanks-text'>Thanks for your opinion. You make OpenOogle better!</span>
                        :
                        <button className='eval' onClick={()=>setEvaluator(!evaluator)}>
                            Evaluate
                        </button>}
        </div>
    )
}

export default ResultPage;
