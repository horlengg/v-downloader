
window.addEventListener('DOMContentLoaded', () => {
    appLoaded()
})

let isDownloading = false;

function appLoaded() {
    const listButtonDownload = document.getElementsByClassName("btn-download")
    if(!listButtonDownload || !listButtonDownload.length) return
    Array.from(listButtonDownload)
    .forEach(button=>{
        button.addEventListener("click",()=>{
            const videoUrl = button.getAttribute("data-url")
            download(videoUrl,button)
        })
    })
}

async function download(url,button){
    if(!url) return;
    if(isDownloading) {
        return alert("Already downloading a video, Please wait for the current download to finish.");
    }
    setLoadingToClient(button)
    const response = await fetch(url,{method : "POST"});
    if (!response.ok) {
        alert("Failed to fetch video");
        removeLoadingToClient(button)
        return;
    }
    const blob = await response.blob();

    removeLoadingToClient(button)

    const blobUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.href = blobUrl;
    link.download = `idownload-${Date.now()}.${blob.type.includes('audio') ? 'mp3' : 'mp4'}`
    link.click();
    link.remove();
}

function setLoadingToClient(element){
    isDownloading = true
    element.setAttribute("disabled",true)
    element.classList.add("is_loading")
}
function removeLoadingToClient(element){
    isDownloading = false
    element.removeAttribute("disabled"); 
    element.classList.remove("is_loading")
}
