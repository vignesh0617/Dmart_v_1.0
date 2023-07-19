
document.onclick=()=>{
    
    try{
        document.getElementById("submit_button").onclick=()=>{
            console.log("Clicked submit button")
        }
    }catch{
        console.log("Submit botton not present in this page")
    }
}
