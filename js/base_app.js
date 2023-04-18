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




