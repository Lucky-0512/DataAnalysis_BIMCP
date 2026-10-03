
// so whenever the user enters intot h chatbox, and either hits enter or clicks on the arrow icon, we need to do 3 things.

// 1. add this message as a simple div UI to the convo section [to the right]
// 2. send this query as a payload to python via POST request , and add it to chat_history, runn call and get back the response that is stream from serve to here contineously.
// 3. and after rendering the respnse here, add it to chat history s assitant message.


// get the textinput element
const textbox = document.querySelector("#prompt")

// getthe snd element
const arrow = document.querySelector("#send")

const converstaions = document.querySelector("#conversation") // parent div thatholds the user and assistant messages

const fileIp = document.querySelector("#user-file")

const formIP = document.querySelector("#attform")
    
// create formData object to access he   files a all data from the form.
const FormD = new FormData(formIP)

function handleAttchments(){

    fileIp.addEventListener("change",()=>{
        // check for non empty selection.
        if(!fileIp.files.length || fileIp.files.length === 0){
            // delete the default empty file object in the formdata first.
            FormD.delete("uploaded_file")
            
        }
        
        else{
            console.log("file selection being submitted from JS....")
            // trigger the submit event on form element.
            formIP.requestSubmit()

        }
        console.log(FormD)

    })

    // now handling the submission, ne it got triggered.
    formIP.addEventListener("submit",(e)=>{
        e.preventDefault()
        
        // gets all the files selected from te input box element,iterate over each append to fromdata. "uploaded_file" referes to the name= attribte in the input box
       
        for (const f of fileIp.files){
            FormD.append("uploaded_file",f)
        }
                
    })

}

handleAttchments()   // if any such events are triggered , it'all apply the attachment logic.

async function post_query() {
      
    // get the user query text.
    const query = textbox.value

    textbox.value = ''   // empty the text input

    // first let's append this query to the user side UI box.
    const user_div = document.createElement("div")
    user_div.className = "users"

    // create an assitant ui

    function set_ui_styles(user_div){
    user_div.style.width = "auto"
    user_div.style.maxWidth = "40%"
    user_div.style.backgroundColor = "white"
    user_div.style.color = "black"
    user_div.style.fontFamily = "monospace"
    user_div.style.fontSize = "medium"
    user_div.style.borderRadius = "5px"
    user_div.style.height = "auto"

    if(user_div.className == 'users'){
        user_div.style.alignSelf = "flex-end"

    }
    else{
        user_div.style.alignSelf = "flex-start"

    }
    

    } 

    set_ui_styles(user_div)
    user_div.textContent = query
    converstaions.appendChild(user_div)


    // let's create an assistant ui.
    const ass_ui = document.createElement("div")
    ass_ui.className = "assistant"
    set_ui_styles(ass_ui)

    // first append to the convo div => then update the contents....
    converstaions.appendChild(ass_ui)

    // now calling the model from sevr for the respnse.
    FormD.append("query",query) // adding query attribute to frmdata object to store user query.

    const res = await fetch("/query/user",{
        method : "POST",
        // append the query into formdata object.
        body : FormD
        })

        // now lets catch the dropping chunks via reader.
        const Reader = res.body.getReader()

        while(true){
            // keep collecting them.
            const {value,done} =await Reader.read()  // note: use the keyword 'value' onlyyyyy.

            if(done){
                // break the loop it stream ends from the server.
                console.log("streaming completed!")
                break
                }

            // now let's decode the chunk.
            const decoder = new TextDecoder()
                        
            const word  = decoder.decode(value,{stream:true})

            // append this word to the innercontent of the assistant ms UI.
                ass_ui.textContent += word



        }
    
    }



    // now adding the event listener to listen for both click or enter events.
    arrow.addEventListener("click",(e)=>{
        e.preventDefault()
        post_query()
    })
    textbox.addEventListener("keydown",(e)=>{
        if (e.key == "Enter"){
            e.preventDefault()
            post_query()
        }

    })
    

