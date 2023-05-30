import {Rating} from '@mui/material';
import {useState} from 'react';
import './ResultPage.css';
const ResultPage = ({rank, link, snippet, title}) => {
    const [evaluator, setEvaluator] = useState(false);

    return (
        <div className='page-result'>
            <p>{rank}</p>
            <span className='pure-link'>{link}</span>
            <a href={link}>{title}</a>
            <p>{snippet}</p>
            {evaluator?
                <Rating name="size-medium" defaultValue={2.5} precision={0.5}/>
                :
                <button onClick={()=>setEvaluator(!evaluator)}>Evaluate</button>}
        </div>
    )
}

export default ResultPage;
