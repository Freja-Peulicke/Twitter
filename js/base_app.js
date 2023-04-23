// ##############################

function showTip(message){
    const tip_id = Math.random()
    let tip = `
    <div data-tip-id="${tip_id}" class="flex justify-center w-full lg:w-1/3 mx-auto py-4 text-white bg-purple-500 rounded-md">
      ${message}
    </div>
    `
    document.querySelector("#tips").insertAdjacentHTML("afterbegin", tip)
    setTimeout(function(){
        document.querySelector(`[data-tip-id='${tip_id}']`).remove()
    }, 3000)
}

// ##############################

async function sign_up(){
    const btn = event.target
    btn.disabled = true
    btn.innerText = btn.getAttribute("data-await")
    const frm = event.target.form
    const conn = await fetch ("/api-sign-up", {
        method : "POST",
        body: new FormData(frm)
    })
    btn.disabled = false
    btn.innerText = btn.getAttribute("data-default")
    if( !conn.ok ){
        console.log("Cannot sign up")
        showTip("Cannot sign up")        
        return
    }
    const data = await conn.json()
    // Success
    location.href = `/`
}


async function login(){
    const btn = event.target
    btn.disabled = true
    btn.innerText = btn.getAttribute("data-await")
    const frm = event.target.form
    // Kilde: https://stackoverflow.com/a/47604112 brugt for at jeg kunne få response json ud selv ved 400 bad request
    const conn = await fetch("/api-login", {
        method : "POST",
        body : new FormData(frm)
    }).then((response) => {
        if(response.ok){
            return response;
        }else{
            return response.json().then((data) => {
                return data;
            }).catch((err) => {
                console.log(err);
            })
        } 
    })
    btn.disabled = false
    btn.innerText = btn.getAttribute("data-default")
    if( !conn.ok ){
        console.log("Cannot login: " + conn.info)    
        showTip(conn.info)
        return
    }
    const data = await conn.json()
    // Success
    location.href = `/${data.user_name}`
}


async function tweet(){
    const frm = event.target // the form
    const conn = await fetch("/tweet", {
      method: "POST",
      body: new FormData(frm)
    })
    // const data = await conn.text() // to get plain text
    const data = await conn.json() // to get plain text
    console.log(data)
    const message = frm.querySelector("input[name='message']").value
    console.log(message)
    document.querySelector("#tweets").insertAdjacentHTML("afterbegin", 
    `<div class="tweet">
        <div>${data.tweet_id}</div>
        <div>${message}</div>  
      </div>`)
  }

  ///////////////////////////////////////////////

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
        // loop and show the tweets in the div
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

//////////////////////////////////////////////////////

async function follow_unfollow(){
    const btn = event.target
    const followee_id = btn.dataset.user
	const api = btn.innerText == "Follow" ? "/api-follow" : "/api-unfollow"
	const dom_profile_total_followers = document.querySelector("#profile_total_followers")
    btn.disabled = true
    
    const conn = await fetch(api,{
        method : "POST",
        headers: {"Content-Type":"application/json"},
        body: '{"followee": "'+followee_id+'"}'
    })
    
	const data = await conn.json()
    if( !conn.ok ){
        console.log(data)
        showTip(data.info)        
        return
    }
	if(api == "/api-follow"){
		dom_profile_total_followers.innerText = parseInt(dom_profile_total_followers.innerText) + 1
	}else{
		dom_profile_total_followers.innerText = parseInt(dom_profile_total_followers.innerText) - 1 
	}
    //shorthand if (forkortet if/else statement)
	btn.innerText = api == "/api-follow" ? "Unfollow" : "Follow"    
    btn.disabled = false
    // Success
    console.log("ok follow")
}


//////////////////////////////////////////////////////

async function like_unlike_tweet(){
    const btn = event.currentTarget
    const tweet_id = btn.dataset.tweet
    const api = btn.dataset.liked === "0" ? "/api-like" : "/api-unlike"
    const dom_tweet_likes = btn.lastElementChild
    const svg = btn.firstElementChild.firstElementChild

    const conn = await fetch(api,{
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: '{"type": "tweet", "tweet_id": "'+tweet_id+'"}'
    })

    const data = await conn.json()
    if( !conn.ok ){
        console.log(data)
        showTip(data.info)        
        return
    }

    if(api == "/api-like"){
		dom_tweet_likes.innerText = parseInt(dom_tweet_likes.innerText) + 1
        svg.classList.remove("show-unliked")
        svg.classList.add("show-liked")
        btn.dataset.liked = "1"
	}else{
		dom_tweet_likes.innerText = parseInt(dom_tweet_likes.innerText) - 1 
        svg.classList.remove("show-liked")
        svg.classList.add("show-unliked")
        btn.dataset.liked = "0"
	}
    console.log("ok like")
}


//////////////////////////////////////////////////////

async function send_gold_code(){
    const btn = event.currentTarget
    btn.disabled = true
    const conn = await fetch("/api-gold",{
        method: "POST"
    })

    const data = await conn.json()
    if( !conn.ok ){
        console.log(data)
        showTip(data.info)        
        return
    }
    let step_2 = document.querySelector("#step-2")
    step_2.classList.remove("hidden")
    step_2.classList.add("flex")

}

async function verify_gold_code(){
    const btn = event.currentTarget 
    btn.disabled = true
    let digit_1 = document.querySelector("#digit-1").value
    let digit_2 = document.querySelector("#digit-2").value
    let digit_3 = document.querySelector("#digit-3").value
    let digit_4 = document.querySelector("#digit-4").value
    let verify_code = digit_1 + digit_2 + digit_3 + digit_4 
    const conn = await fetch("/api-gold-verify",{
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: '{"verify_code": "'+verify_code+'"}'
    })

    const data = await conn.json()
    if( !conn.ok ){
        console.log(data)
        showTip(data.info)        
        return
    }

    let step_1 = document.querySelector("#step-1")
    step_1.classList.add("hidden")
    let step_2 = document.querySelector("#step-2")
    step_2.classList.add("hidden")
    step_2.classList.remove("flex")
    let gold_memmber = document.querySelector("#gold-member")
    gold_memmber.classList.remove("hidden")
    gold_memmber.classList.add("flex")
}