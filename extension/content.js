var i;
var str = "\/\/*[@id=\"react-root\"]\/div\/div\/div[2]\/main\/div\/div\/div\/div\/div\/div[2]\/div\/div\/section\/div\/div\/div["    
var URL = document.URL;
var apiURL = ""

function send(trending_topic, apiURL){
    fetch( apiURL,{
        method: 'POST',
        body: JSON.stringify(trending_topic),
        headers:{
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        } })
        .then(data => {return data.json()})
        .then(res => {return res})
}

function positiveScore(score,element){
    var y = (51/500)*(score-100)**2;
    var yS = y.toString();
    element.style.color = "rgb(" +yS +", 255," + yS+")";
}

function negativeScore(score, element){
    var y = (51/500)*(score)**2;
    var yS = y.toString();
    
    element.style.color = "rgb( 255, " +yS +", " + yS+")"; 

}

function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
  }

function trends(){ 
    setTimeout(function() {
        if(URL.includes("twitter") && URL.includes("trending")){
            
                for(i = 3; i < 33; i++){
                    
                    try{
                        var str2 = "]\/div\/div\/div\/div[2]\/span\/span"
                        var s = i.toString(); 
                
                        var final = str.concat(s,str2);
                        var element = getElementByXpath(final)

                        //console.log(element)
                        //console.log(element.innerHTML = element.innerText || element.textContent);
                        
                        const trending_topic = element.innerText || element.textContent;
                        
                        var score = send(trending_topic, apiURL);
                        
                        if(score >= 50){
                            positiveScore(score,element)
                        }
                        
                        else{
                            negativeScore(score,element);
                        }                   


                    }
                    
                    catch(err){
                        var str2 = "]\/div\/div\/div\/div[2]\/span"
                        var s = i.toString();
                
                        var final = str.concat(s,str2);
                        var element = getElementByXpath(final)

                        //console.log(element)
                        //console.log(element.innerHTML = element.textContent)
                        const trending_topic = element.textContent;
                        var score = send(trending_topic, apiURL);
                        
                        if(score >= 50){
                            positiveScore(score,element)
                        }
                        
                        else{
                            try{
                                negativeScore(score,element);
                            }
                            catch(e){break;}
                        }

                    }
                    
                }
            
        } 
    }, 3000)
}

trends()
function recursive(){
    trends()
    setTimeout(recursive, 60000);
}
recursive();


    
