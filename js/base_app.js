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
    const conn = await fetch("/api-login", {
        method : "POST",
        body : new FormData(frm)
    })
    btn.disabled = false
    btn.innerText = btn.getAttribute("data-default")
    if( !conn.ok ){
        console.log("Cannot login")
        showTip("Invalid credentials. Try again")        
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

//////////////////////////////////////////////////////

async function follow_unfollow(followee_id){
    const btn = event.target
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



