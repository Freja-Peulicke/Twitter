async function admin_block_unblock_user(){
    const btn = event.target
    const user_id = btn.dataset.user

    btn.disabled = true
    
    const conn = await fetch("/api-admin-block-unblock-user",{
        method : "POST",
        headers: {"Content-Type":"application/json"},
        body: '{"user_id": "'+user_id+'"}'
    })

    const data = await conn.json()
    if( !conn.ok ){
        console.log(data)
        showTip(data.info)        
        return
    }

    btn.disabled = false
    window.location.reload()
}

///////////////////////////////////////////


async function admin_delete_user(){
    const btn = event.target
    const user_id = btn.dataset.user

    btn.disabled = true
    
    const conn = await fetch("/api-admin-delete-user",{
        method : "POST",
        headers: {"Content-Type":"application/json"},
        body: '{"user_id": "'+user_id+'"}'
    })

    const data = await conn.json()
    if( !conn.ok ){
        console.log(data)
        showTip(data.info)        
        return
    }

    btn.disabled = false
    window.location.reload()
}