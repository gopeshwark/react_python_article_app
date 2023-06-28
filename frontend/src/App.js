import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [articles, setArticles] = useState([])
  useEffect(() => {
    fetch('http://127.0.0.1:5000/get', {
      'methods': 'GET',
      headers: {
        'Content-Type': "applications/json"
      }
    }).then(resp => resp.json()).then(resp => setArticles(resp)).catch(error => console.log(error))
  }, [])
  return (
    <div className="App">
      <h1>Flask and ReactJS Course</h1>
      {articles?.map(article => {
        return (
          <div key={article?.id}>
            <h2>{article?.title}</h2>
            <p>{article?.body}</p>
            <p>{article?.date}</p>
          </div>
        )
      })}
    </div>
  );
}

export default App;
