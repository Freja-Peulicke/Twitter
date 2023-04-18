function show_search_results(){
    if(document.querySelector("#search_results").innerHTML != ""){
        document.querySelector("#search_results").classList.remove("hidden")
    }
}

function hide_search_results(){
    document.querySelector("#search_results").classList.add("hidden")
}

let the_timer;
function search(){
    clearTimeout(the_timer);
    the_timer = setTimeout( async function(){
        let query = document.querySelector("#search_input").value;
        const conn = await fetch("/search",{
            method : "POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: '{"query": "'+query+'"}'
        })
        const data = await conn.json()
        console.log(data)
        // loop and shop the names in the div
        let results = ""
        document.querySelector("#search_results").innerHTML = ""
        data.forEach( (item)=>{
            if(item.hasOwnProperty('tweet_message')){
                console.log(item.tweet_message)
                results += `<div class="text-sm mb-3 text-black">${item.tweet_message}</div>`
            }
        })
        document.querySelector("#search_results").insertAdjacentHTML('afterbegin',results);
        show_search_results();
    }, 500 );
}
