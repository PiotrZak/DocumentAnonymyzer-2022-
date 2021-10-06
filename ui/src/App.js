import './App.css';
import logo from './logo.svg';
import React, { useState } from 'react';
import {FileUpload} from './FileUploader';

const apiUrl = "http://localhost:5000";
const developmentUrl = "https://hack4law-api.azurewebsites.net";
const url1 = apiUrl + "/api/v1/switch"
const url2 = apiUrl + "/api/v1/ner"
const url3 = apiUrl + "/api/v1/displacy"

console.log("PYTHON_API_URL is set to: " + apiUrl)

export const App = () => {

  const [text, setText] = useState("");
  const [transformedText, setTransformedText] = useState("");
  const [anonymysedPhrases, setAnonymysedPhrases] = useState([]);
  const [categories, setCategories] = useState([]);
  const [textWithLabel, setTextWithLabel] = useState();
  const [isFull, setIsFull] = useState();

  const [active, setActive] = useState([]);

  const anonymyse = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    };

    fetch(url1, requestOptions)
      .then((response) => response.json()).then((responseJson) => {
        setTransformedText(responseJson)
      })
    getAnonymysedData()
  }

  const getAnonymysedData = () => {

    setActive([])
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    };
    fetch(url2, requestOptions)
      .then((response) => response.json()).then((responseJson) => {
        const uniqueCategories = [];
        console.log(responseJson)
        responseJson.map((category) => {
          if (uniqueCategories.indexOf(category.label) === -1) {
            uniqueCategories.push(category.label)
          }
        });
        setCategories(uniqueCategories)
        setAnonymysedPhrases(responseJson);
      })
  }

  const getPhrasesByCategory = (category, key) => {
    if (active.includes(key)) {
      setActive(active.filter(x => x !== key));
      anonymyseByCategory(anonymysedPhrases.filter(x => x.label === category), false);
    }
    else {
      setActive([...active, key]);
      anonymyseByCategory(anonymysedPhrases.filter(x => x.label === category), true);
    }
  }

  const showFullText = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    };

    fetch(url3, requestOptions)
      .then((response) => response.json()).then((responseJson) => {
        setTextWithLabel(responseJson)
      })
      setIsFull(!isFull)
  }

  const anonymyseByCategory = (phrasesByCategory, visible) => {
    const textArray = [transformedText];
    for (const i in phrasesByCategory) {
      const startIndex = phrasesByCategory[i].start_char;
      const endIndex = phrasesByCategory[i].end_char;
      let hiddenText = visible
        ? textArray[i].substring(startIndex, endIndex)
        : textArray[i].substring(startIndex, endIndex).replace(textArray[i].substring(startIndex, endIndex), 'X'.repeat(textArray[i].substring(startIndex, endIndex).length))
      const visibleText = text.substring(startIndex, endIndex);
      const sentenceWithReplacedPhrases = visible
        ? replaceAt(textArray[i], hiddenText, visibleText, startIndex, endIndex)
        : replaceAt(textArray[i], visibleText, hiddenText, startIndex, endIndex)
      textArray.push(sentenceWithReplacedPhrases)
      setTransformedText(sentenceWithReplacedPhrases);
    }
  }

  function replaceAt(input, search, replace, start, end) {
    return input.slice(0, start) +
      input.slice(start, end).replace(search, replace) +
      input.slice(end);
  }

  return (
    <div className="container">
      <div className="container__left">
      <img src={logo} className="App-logo" alt="logo" />
        <FileUpload/>
        <input className="form-field" type="text" placeholder="Write text to anonymyse" name="name" onChange={e => setText(e.target.value)} />
        <button className="submit-feedback" onClick={() => anonymyse()}>Anonymyse</button>

        <p onClick={() => showFullText()}>Show words</p>

        <h3>Categories:</h3>
        {categories.map((x, i) => {
          return (
            <p className={active.includes(i) ? 'active' : ''} key={i} onClick={() => getPhrasesByCategory(x, i)}>{x}</p>
          )
        })}

      </div>
      <div className="container__right">
        {isFull ? <div dangerouslySetInnerHTML={{ __html: textWithLabel }} /> : <p>{ transformedText }</p>}
      </div>

    </div>
  )
}
