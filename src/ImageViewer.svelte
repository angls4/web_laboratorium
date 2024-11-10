<script>
    export let fileType='';
    export let fileUrl='';
    export let fileName='';

    let blobUrl='';
    let originalHeight = 21;
    let originalWidth = 14;

    let zoomScale = 1;
    function showVal(a) {
        const val = a.target.value;
        zoomScale = Number(val) / 10;
    }
    function onWheel(ev) {
        if (!originalHeight || !originalWidth) return;
        console.log('wheel');
        if (ev.ctrlKey) {
            ev.preventDefault();
            zoomScale -= ev.deltaY * 0.001 * Math.sqrt(zoomScale);
            if (zoomScale < 0.1) zoomScale = 0.1;
        }
    }
    async function fileUrlToBlobUrl(fileUrl) {
        try {
            // Fetch the file from the URL
            const response = await fetch(fileUrl);

            // Check if the fetch was successful
            if (!response.ok) throw new Error("Network response was not ok");

            // Convert the response to a Blob
            const blob = await response.blob();

            // Set the original width and height of the image
            

            // Create a Blob URL
            blobUrl = URL.createObjectURL(blob);
            // zoomScale = 0.7;
            return blobUrl;
        } catch (error) {
            console.error("Error converting file URL to Blob URL:", error);
            blobUrl = '';
            return blobUrl;
        }
    }
    // $: {
    //     fileUrlToBlobUrl(fileUrl);
    // }

</script>
{#await fileUrlToBlobUrl(fileUrl)}
    <div>Loading...</div>
{:then}  
{#if blobUrl}
<div class="download">
    <a href={blobUrl} download={fileName.split('/').pop()}>
        <button>Download</button>
    </a>
</div>
{#if fileType ? fileType.includes('image') : false}
    <input class="zoom-range" id="test" min="1" max="10" value={zoomScale*10} step="1" type="range" on:input={showVal}/>
    <div on:wheel={onWheel} class="image-container">
        <div class="image-wrapper">
            <img
            class="image"
            src={blobUrl}
            alt="failed loading image"
            bind:naturalHeight={originalHeight}
            bind:naturalWidth={originalWidth}
            style={`width: ${zoomScale * originalWidth}px; height: ${zoomScale * originalHeight}px;`}
            />
        </div>
    </div>
    
{:else if fileType == 'application/pdf'}
    <object class="pdf" data={blobUrl} type={fileType}></object>
{:else}
    <div>Unsupported file type</div>
{/if}
{:else}
    <div>Failed to load image</div>
{/if}
{/await}

<style>
    .zoom-range {
        -webkit-appearance: none;
        width: 200px;
        height: 3px;
        background: #007bff;
        outline: none;
        opacity: 0.7;
        transition: opacity .15s ease-in-out;
        margin-bottom: 10px;
    }

    .zoom-range:hover {
        opacity: 1;
    }

    .zoom-range::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        background: #007bff;
        cursor: pointer;
        border-radius: 50%;
    }

    .zoom-range::-moz-range-thumb {
        width: 20px;
        height: 20px;
        background: #007bff;
        cursor: pointer;
        border-radius: 50%;
    }
    .image-container {
        width: 100%;
        height: calc(97%);
        max-height: 80vh;
        margin-bottom: 0;
        overflow: scroll;
        display: flex;
        justify-content: center;
    }
    .image-wrapper {
        width: max-content;
        height: max-content;
        display: flex;
    }
    .download {
        text-align: center;
        margin-bottom: 0;
    }

    .download button {
        background-color: #007bff;
        margin-top: 0;
        margin-bottom: 10px;
        font-size: small;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        text-decoration: none;
        transition: background-color 0.3s ease;
    }

    .download button:hover {
        background-color: #0056b3;
    }
    .image {
        display: block;
    }
    .pdf {
        width: 100%;
        height: 80vh;
    }
</style>
