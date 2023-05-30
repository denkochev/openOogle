import './ResultPage.css';
const ResultPage = ({rank, link, snippet, title}) => {

    return (
        <div className='page-result'>
            <p>{rank}</p>
            <span className='pure-link'>{link}</span>
            <a href={link}>{title}</a>
            <p>{snippet}</p>
        </div>
    )
}

export default ResultPage;
