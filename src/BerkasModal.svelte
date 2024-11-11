<script>
    import ImageViewer from './ImageViewer.svelte';
    import { addBerkas, getBerkas, getBerkases, getPendaftaran, komentarBerkas } from './BerkasApi';

    export let isOpen = false;
    export let pendaftaran = {};
    export let berkasesList = [];
    export let ticker = 1;
    export let rows = [];
    export let user = {};

    let selectedJenis;
    let selectedBerkases;
    let selectedBerkas;

    // input
    let selectedFile;   
    let newKomentar = '';

    export function changePendaftaran(newPendaftaran, newBerkasesList) {
        pendaftaran = newPendaftaran
        berkasesList = newBerkasesList;
        selectedJenis = null;
        selectedBerkases = null;
        selectedBerkas = null;
    }
    export function openModal() {
        isOpen = true;
    }

    export function closeModal() {
        isOpen = false;
    }
 
    function changeJenis(jenis) {
        selectedJenis = jenis;
        console.log(selectedJenis);
    }
    function changeBerkases(berkases) {
        selectedBerkases = berkases;
        selectedJenis = berkases.value;
        selectedBerkas = berkases.berkases[0];
        console.log(selectedBerkases);
    }
    function changeBerkas(berkas) {
        selectedBerkas = berkas;
        console.log(selectedBerkas);
    }
    function revisionLabel(revision) {
        console.log(revision);
        if(ticker)
            return revision == 2 ? "direvisi" : revision == 1 ? "perlu revisi" : "";
    }

  
    let fetching = false;
    async function handleAddBerkas(el) {
        if (fetching) return
        if (selectedFile && selectedJenis) {
            try {
                fetching = true;
                const response = await addBerkas(pendaftaran, selectedJenis, selectedFile);
                if (response.status === 200) {
                    selectedFile = null;
                    alert('Berkas added successfully');
                    // Refresh the berkases list or update the UI accordingly   
                    const newBerkases = await getBerkases(pendaftaran, selectedJenis)
                    berkasesList[berkasesList.indexOf(selectedBerkases)].revision = newBerkases.revision
                    berkasesList[berkasesList.indexOf(selectedBerkases)].berkases = newBerkases.berkases
                    changeBerkas(selectedBerkases.berkases[0]);
                    const newPendaftaran = await getPendaftaran(pendaftaran.id);
                    rows[rows.findIndex(row=>row.id==pendaftaran.id)] = newPendaftaran.pendaftaran;
                    console.log("revised rows",rows)
                } else {
                    alert('Failed to add berkas');
                }
            } catch (error) {
                console.error('Error adding berkas:', error);
                alert('Error adding berkas');
            }
        } else {
            alert('Please select a file and jenis');
        }
        fetching = false
    }

    function handleFileChange(event) {
        selectedFile = event.target.files[0];
        handleAddBerkas()
    }


    async function handleAddKomentar(el) {
        if (fetching) return
        if (newKomentar && selectedBerkas) {
            try {
                fetching = true
                const response = await komentarBerkas(selectedBerkas, newKomentar);
                if (response.status === 200) {
                    newKomentar = '';
                    alert('Komentar added successfully');
                    // Refresh the komentars list or update the UI accordingly
                    const newBerkas = await getBerkas(selectedBerkas.id);
                    selectedBerkas.komentars = newBerkas.berkas.komentars
                    berkasesList[berkasesList.indexOf(selectedBerkases)].revision = newBerkas.revision
                    console.log(newBerkas)
                    const newPendaftaran = await getPendaftaran(pendaftaran.id);
                    rows[rows.findIndex(row=>row.id==pendaftaran.id)] = newPendaftaran.pendaftaran;
                } else {
                    alert('Failed to add komentar');
                }
            } catch (error) {
                console.error('Error adding komentar:', error);
                alert('Error adding komentar');
            }
        } else {
            alert('Please enter a komentar');
        }
        fetching = false
    }
    const forceUpdate = async (_) => {};
</script>



{#if isOpen}
    <div class="overlay">
        <dialog class="modal" open>
            <div class="header-container">
                <div class="close-button">
                    <button style="opacity: 0; cursor:default;">&times;</button>
                </div>
                <div class="header"><h1><slot name="header">HEADER MODAL</slot></h1></div>
                <div class="close-button">
                    <button on:click={closeModal}>&times;</button>
                </div>
                <!-- <div class="close-button">
                    <button on:click={()=>console.log(pendaftaran,berkasesList)}>tes</button>
                </div> -->
            </div>
            <div class="body-container">
                <div class="jenis-container">
                    {#await forceUpdate(ticker) then _}
                    {#each berkasesList as berkases}
                        <a on:click={()=>ticker++}></a>
                        <div class="jenis-chip {selectedBerkases?.value == berkases?.value ? "selected" : ""}" on:click={()=>changeBerkases(berkases)}>
                            <p>{berkases.label}</p>
                            <p>{!berkases.berkases[0] ? "tidak ada" : ""}</p>
                            <p>{revisionLabel(berkases.revision)}</p>
                        </div>
                    {/each}
                    {/await}
                </div>
                <div class="berkas-container">
                    {#if selectedBerkases}
                    {#if user.id == pendaftaran.user_id || user.is_superuser}
                    <div class="add-berkas">
                        <label for="fileInput" class="file-label">Upload Berkas</label>
                        <input hidden type="file" accept=".pdf, .jpg, .jpeg, .png, .webp" id="fileInput" on:change={handleFileChange} class="file-input" />
                        <!-- <button on:click={handleAddBerkas} class="add-berkas-button">Add Berkas</button> -->
                    </div>
                    {/if}
                        {#if selectedBerkas}
                        
                            <div class="berkas-navigation">
                                <button 
                                    on:click={() => changeBerkas(selectedBerkases.berkases[selectedBerkases.berkases.indexOf(selectedBerkas) + 1])}
                                    disabled={selectedBerkases.berkases.indexOf(selectedBerkas) === selectedBerkases.berkases.length - 1}>
                                    &larr; Previous
                                </button>
                                <h2>{selectedBerkas.uploaded_at}</h2>
                                <h2>Berkas {selectedBerkases.berkases.length - selectedBerkases.berkases.indexOf(selectedBerkas)}/{selectedBerkases.berkases.length}</h2>
                                <button 
                                    on:click={() => changeBerkas(selectedBerkases.berkases[selectedBerkases.berkases.indexOf(selectedBerkas) - 1])}
                                    disabled={selectedBerkases.berkases.indexOf(selectedBerkas) === 0}>
                                    Next &rarr;
                                </button>
                            </div>
                        
                        <div class="berkas">
                            {#await forceUpdate(ticker) then _}
                            {#if selectedBerkas.komentars?.length > 0}
                            <h2>Revisi</h2>
                            {#each selectedBerkas.komentars as komentar}
                            <div class="komentar">
                                <p>{komentar.content}</p>
                                <small>By {komentar.user}</small>
                                <small>{komentar.created_at}</small>
                            </div>
                            {:else}
                            <p>Tidak ada revisi</p>
                            {/each}
                            {/if}
                            {/await}
                            <ImageViewer fileType={selectedBerkas.file_type} fileUrl={selectedBerkas.file_url} fileName={selectedBerkas.file_name} />
                            {#if user.koordinator}
                            <div class="revisi-container">
                                <textarea height="100px" bind:value={newKomentar} placeholder="Tambahkan revisi atau komentar disini..."></textarea>
                                <button on:click={handleAddKomentar}>Tambah Revisi</button>
                            </div>
                            {/if}
                        </div>
                        {:else}
                        <p>Berkas tidak ada</p>
                        {/if}
                    {:else}
                        <p>Pilih jenis berkas</p>
                    {/if}
                </div>
            </div>
            
            
        </dialog>
    </div>
{/if}

<style>
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        max-width: 90%;
        max-height: 90%;
        /* overflow: hidden; */
        display: flex;
        flex-direction: column;
        width: 80vw;
        height: 90vh;
    }
    

    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        margin-bottom: 1rem;
    }
    .header {
        flex: 1;
    }
    .body-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 1;
        overflow: scroll;
    }
    .header-container h1 {
        margin: 0;
        font-size: larger;
    }
    .close-button {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: black;
        padding: 0;
    }
    .close-button button {
        font-size: smaller !important;
        margin: 0;
        padding: 2px 8px;
    }
    .jenis-container {
        /* margin-top: 2rem; */
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center ;
        width: 100%;
    }
    .jenis-chip {
        background-color: #f1f1f1;
        cursor: pointer;
        color: black;
        margin: 5px;
        padding: 5px 10px;
        border-radius: 5px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .jenis-chip.selected {
        border: 1px solid #007bff;
        /* border-color: #007bff; */
        /* color: white; */
    }
    

    .berkas-container {
        display: flex;
        /* height: 40%; */
        width: 100%;
        flex-direction: column;
        align-items: center;
        margin-top: 5px;
        flex: 1;
        align-self: stretch;
        /* overflow: hidden; */
    }
    .berkas-navigation {
        display: flex;
        justify-content: space-between;
        width: 100%;
        max-width: 600px;
        margin-bottom: 5px;
    }
    .berkas-navigation button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        padding: 0px;
        border-radius: 5px;
        color : #007bff;
        margin: 0
    }
    .berkas-navigation button:disabled {
        color: #ccc;
    }
    .berkas {
        display: flex;
        flex-direction: column;
        /* padding: 10px; */
        align-items: center;
        /* margin-top: 20px; */
        width: 98%;
        overflow: hidden;
        flex: 1;
        height: 75vh;
    }
    .add-berkas {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 5px;
    }

    .file-label {
        background-color: #007bff;
        cursor: pointer;
        margin-top: 0;
        margin-bottom: 10px;
        font-size: small;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        text-decoration: none;
        transition: background-color 0.3s ease;
    }

    .file-label:hover {
        background-color: #0056b3;
    }

    .add-berkas-button {
        background-color: #28a745;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .add-berkas-button:hover {
        background-color: #218838;
    }
   

    .berkas-viewer {
        margin-bottom: 20px;
    }

    .revisi-container {
        margin-top: 10px;
        width: 100%;
        max-width: 600px;
        display: flex;
        align-items: center;
    }
    .revisi-container button {
        background: #007bff;
        border: none;
        cursor: pointer;
        color: white;
        font-size: 0.8rem;
        padding: 5px 10px;
        border-radius: 3px;
        transition: background-color 0.3s ease;
        margin: 0;
    }
    .revisi-container textarea {
        width: 100%;
        padding: 5px;
        border-radius: 3px;
        border: 1px solid #ccc;
        margin-right: 5px;
    }

    .revisi-container button:hover {
        background-color: #0056b3;
    }

    .komentar {
        background-color: #f1f1f1;
        border: 1px solid #ccc;
        padding: 8px;
        margin-bottom: 16px;
        margin-top: 8px;
        border-radius: 4px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        word-wrap: break-word;
        max-width: 80%;
    }

    .komentar p {
        margin: 0;
        max-width: 100%;
        font-size: 0.9rem;
        color: #333;
        word-wrap: break-word;
    }

    .komentar small {
        margin-top: 4px;
        font-size: 0.8rem;
        color: #777;
        word-wrap: break-word;
    }

</style>
<!-- <button on:click={openModal}>Open Modal</button> -->