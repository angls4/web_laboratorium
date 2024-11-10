<script>
  import { getPendaftaran, nextStatus, setNilaiStatus } from "./BerkasAPI";

    export let isOpen = false;
    let pendaftaran;
    export let rows;
    // let jsonTesMicroteaching; // selection_status 2
    // let jsonTesPemahaman; // selection_status 3
    // let jsonWawancaraAsisten; // selection_status 4
    // let jsonWawancaraDosen; // selection_status 5
    let selection_status = 0;
    // export let jsonWawancaraDosen = { pd: 5, rrd: 5, mdb: 5, komentar: "Bagus" };
    let inputTesMicroteaching;
    let inputTesPemahaman;
    let inputWawancaraAsisten;
    let inputWawancaraDosen;


    export function openModal() {
        isOpen = true;
    }

    export function closeModal() {
        isOpen = false;
    }
    export function changePendaftaran(newPendaftaran) {
        pendaftaran = newPendaftaran;
        console.log("pendaftaran di penilaian",pendaftaran);
        // jsonTesMicroteaching = pendaftaran?.nilai_tm; // selection_status 2
        // jsonTesPemahaman = pendaftaran?.nilai_tp; // selection_status 3
        // jsonWawancaraAsisten = pendaftaran?.nilai_wa; // selection_status 4
        // jsonWawancaraDosen = pendaftaran?.nilai_wd; // selection_status 5
        // inputTesMicroteaching = pendaftaran?.nilai_tm ?? { nilai: 0, komentar: "" }; // selection_status 2
        // inputTesPemahaman = pendaftaran?.nilai_tp ?? { pm: 0, km: 0, mk: 0, kmp: 0, sp: 0, komentar: "" }; // selection_status 3
        // inputWawancaraAsisten = pendaftaran?.nilai_wa ?? { pd: 0, rrd: 0, mdb: 0, komentar: "" }; // selection_status 4
        // inputWawancaraDosen = pendaftaran?.nilai_wd ?? { pd: 0, rrd: 0, mdb: 0, komentar: "" }; // selection_status 5
        
        // force structure
        inputTesMicroteaching = {
            nilai: pendaftaran?.nilai_tm?.nilai ?? 0,
            komentar: pendaftaran?.nilai_tm?.komentar ?? ""
        };

        inputTesPemahaman = {
            pm: pendaftaran?.nilai_tp?.pm ?? 0,
            km: pendaftaran?.nilai_tp?.km ?? 0,
            mk: pendaftaran?.nilai_tp?.mk ?? 0,
            kmp: pendaftaran?.nilai_tp?.kmp ?? 0,
            sp: pendaftaran?.nilai_tp?.sp ?? 0,
            komentar: pendaftaran?.nilai_tp?.komentar ?? ""
        };

        inputWawancaraAsisten = {
            pd: pendaftaran?.nilai_wa?.pd ?? 0,
            rrd: pendaftaran?.nilai_wa?.rrd ?? 0,
            mdb: pendaftaran?.nilai_wa?.mdb ?? 0,
            komentar: pendaftaran?.nilai_wa?.komentar ?? ""
        };

        inputWawancaraDosen = {
            pd: pendaftaran?.nilai_wd?.pd ?? 0,
            rrd: pendaftaran?.nilai_wd?.rrd ?? 0,
            mdb: pendaftaran?.nilai_wd?.mdb ?? 0,
            komentar: pendaftaran?.nilai_wd?.komentar ?? ""
        };
        selection_status = pendaftaran?.status_id;
        selectStatus(pendaftaran?.status_id);
    }

    let selectedStatus = 2;
    let selectedData = {};

    function handleInputChange(event, key, type) {
        // if (type === 'microteaching') {
        //     jsonTesMicroteaching[key] = event.target.value;
        // } else if (type === 'pemahaman') {
        //     jsonTesPemahaman[key] = event.target.value;
        // } else if (type === 'wawancaraAsisten') {
        //     jsonWawancaraAsisten[key] = event.target.value;
        // } else if (type === 'wawancaraDosen') {
        //     jsonWawancaraDosen[key] = event.target.value;
        // }
    }

    function selectStatus(jenis) {
        selectedStatus = jenis;
        if (jenis === 2) {
            selectedData = inputTesMicroteaching;
        } else if (jenis === 3) {
            selectedData = inputTesPemahaman;
        } else if (jenis === 4) {
            selectedData = inputWawancaraAsisten;
        } else if (jenis === 5) {
            selectedData = inputWawancaraDosen;
        }
    }
    let fetching = false;
    async function handleSimpan() {
        if (fetching) return;
        try {
            fetching = true;
            const res = await setNilaiStatus(pendaftaran.id, selectedData); 
            if (res && res.status == 200) {
                alert('Berhasil menyimpan data');
                const newPendaftaran = await getPendaftaran(pendaftaran.id);
                rows[rows.indexOf(pendaftaran)] = newPendaftaran.pendaftaran;
                changePendaftaran(newPendaftaran.pendaftaran);
                // closeModal();
            } else {
                alert('Gagal menyimpan data');
            }
        } catch (error) {
            console.error('Error during handleSimpan:', error);
            alert('Terjadi kesalahan saat menyimpan data');
        }
        fetching = false;
    }

    async function handleLanjut() {
        if (fetching) return;
        try {
            fetching = true
            const res = await nextStatus(pendaftaran.id, selectedData);
            if (res && res.status == 200) {
                alert('Berhasil melanjutkan ke status berikutnya');
                const newPendaftaran = await getPendaftaran(pendaftaran.id);
                rows[rows.indexOf(pendaftaran)] = newPendaftaran.pendaftaran;
                changePendaftaran(newPendaftaran.pendaftaran);
                // closeModal();
            } else {
                alert('Gagal melanjutkan ke status berikutnya');
            }
        } catch (error) {
            console.error('Error during handleLanjut:', error);
            alert('Terjadi kesalahan saat melanjutkan ke status berikutnya');
        }
        fetching = false;
    }
</script>

{#if isOpen}
    <div class="overlay">
        <dialog class="modal" open>
            <div class="header-container">
                <div class="close-button">
                    <button style="opacity: 0; cursor:default;">&times;</button>
                </div>
                <div class="header"><h1>Penilaian</h1></div>
                <div class="close-button">
                    <button on:click={closeModal}>&times;</button>
                </div>
            </div>
            <div class="body-container">
                <div class="jenis-container">
                    {#if selection_status === 1}
                        <p>Belum perlu data penilaian</p>
                    {/if}
                    {#if pendaftaran?.nilai_tm || selection_status === 2}
                        <div class="jenis-chip {selectedStatus === 2 ? 'selected' : ''}" on:click={() => selectStatus(2)}>
                            <p>Tes Microteaching</p>
                            {#if selection_status === 2}
                                <p>PERLU DIISI</p>
                            {/if}
                        </div>
                    {/if}
                    {#if pendaftaran?.nilai_tp || selection_status === 3}
                        <div class="jenis-chip {selectedStatus === 3 ? 'selected' : ''}" on:click={() => selectStatus(3)}>
                            <p>Tes Pemahaman</p>
                            {#if selection_status === 3}
                                <p>PERLU DIISI</p>
                            {/if}
                        </div>
                    {/if}
                    {#if pendaftaran?.nilai_wa || selection_status === 4}
                        <div class="jenis-chip {selectedStatus === 4 ? 'selected' : ''}" on:click={() => selectStatus(4)}>
                            <p>Wawancara Asisten</p>
                            {#if selection_status === 4}
                                <p>PERLU DIISI</p>
                            {/if}
                        </div>
                    {/if}
                    {#if pendaftaran?.nilai_wd || selection_status === 5}
                        <div class="jenis-chip {selectedStatus === 5 ? 'selected' : ''}" on:click={() => selectStatus(5)}>
                            <p>Wawancara Dosen</p>
                            {#if selection_status === 5}
                                <p>PERLU DIISI</p>
                            {/if}
                        </div>
                    {/if}
                </div>
                <div class="content-container">
                    {#if selectedStatus === 2}
                        <h2>Tes Microteaching</h2>
                        <label>Nilai: <input type="number" min="1" max="100" bind:value={inputTesMicroteaching.nilai} readonly={selection_status !== 2} on:input={(e) => handleInputChange(e, 'nilai', 'microteaching')} /></label>
                        <label>Komentar: <textarea bind:value={inputTesMicroteaching.komentar} readonly={selection_status !== 2} on:input={(e) => handleInputChange(e, 'komentar', 'microteaching')}></textarea></label>
                        {#if selection_status === 2}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Lanjut</button>
                        </div>
                        {/if}
                    {/if}

                    {#if selectedStatus === 3}
                        <h2>Tes Pemahaman</h2>
                        <label>PM: <input type="number" min="1" max="100" bind:value={inputTesPemahaman.pm} readonly={selection_status !== 3} on:input={(e) => handleInputChange(e, 'pm', 'pemahaman')} /></label>
                        <label>KM: <input type="number" min="1" max="100" bind:value={inputTesPemahaman.km} readonly={selection_status !== 3} on:input={(e) => handleInputChange(e, 'km', 'pemahaman')} /></label>
                        <label>MK: <input type="number" min="1" max="100" bind:value={inputTesPemahaman.mk} readonly={selection_status !== 3} on:input={(e) => handleInputChange(e, 'mk', 'pemahaman')} /></label>
                        <label>KMP: <input type="number" min="1" max="100" bind:value={inputTesPemahaman.kmp} readonly={selection_status !== 3} on:input={(e) => handleInputChange(e, 'kmp', 'pemahaman')} /></label>
                        <label>SP: <input type="number" min="1" max="100" bind:value={inputTesPemahaman.sp} readonly={selection_status !== 3} on:input={(e) => handleInputChange(e, 'sp', 'pemahaman')} /></label>
                        <label>Komentar: <textarea bind:value={inputTesPemahaman.komentar} readonly={selection_status !== 3} on:input={(e) => handleInputChange(e, 'komentar', 'pemahaman')}></textarea></label>
                        {#if selection_status === 3}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Lanjut</button>
                        </div>
                        {/if}
                    {/if}

                    {#if selectedStatus === 4}
                        <h2>Wawancara Asisten</h2>
                        <label>PD: <input type="number" min="1" max="5" bind:value={inputWawancaraAsisten.pd} readonly={selection_status !== 4} on:input={(e) => handleInputChange(e, 'pd', 'wawancaraAsisten')} /></label>
                        <label>RRD: <input type="number" min="1" max="5" bind:value={inputWawancaraAsisten.rrd} readonly={selection_status !== 4} on:input={(e) => handleInputChange(e, 'rrd', 'wawancaraAsisten')} /></label>
                        <label>MDB: <input type="number" min="1" max="5" bind:value={inputWawancaraAsisten.mdb} readonly={selection_status !== 4} on:input={(e) => handleInputChange(e, 'mdb', 'wawancaraAsisten')} /></label>
                        <label>Komentar: <textarea bind:value={inputWawancaraAsisten.komentar} readonly={selection_status !== 4} on:input={(e) => handleInputChange(e, 'komentar', 'wawancaraAsisten')}></textarea></label>
                        {#if selection_status === 4}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Lanjut</button>
                        </div>
                        {/if}
                    {/if}
                    {#if selectedStatus === 5}
                        <h2>Wawancara Dosen</h2>
                        <label>PD: <input type="number" min="1" max="5" bind:value={inputWawancaraDosen.pd} readonly={selection_status !== 5} on:input={(e) => handleInputChange(e, 'pd', 'wawancaraDosen')} /></label>
                        <label>RRD: <input type="number" min="1" max="5" bind:value={inputWawancaraDosen.rrd} readonly={selection_status !== 5} on:input={(e) => handleInputChange(e, 'rrd', 'wawancaraDosen')} /></label>
                        <label>MDB: <input type="number" min="1" max="5" bind:value={inputWawancaraDosen.mdb} readonly={selection_status !== 5} on:input={(e) => handleInputChange(e, 'mdb', 'wawancaraDosen')} /></label>
                        <label>Komentar: <textarea bind:value={inputWawancaraDosen.komentar} readonly={selection_status !== 5} on:input={(e) => handleInputChange(e, 'komentar', 'wawancaraDosen')}></textarea></label>
                        {#if selection_status === 5}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Lanjut</button>
                        </div>
                        {/if}
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
        display: flex;
        flex-direction: column;
        width: 20vw;
        height: 60vh;
    }

    .modal button{
        margin-top: 0%;
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
        /* overflow: scroll; */
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
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
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
    }

    .content-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    .content-container label {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 10px;
        width: 100%;
    }
    .content-container input {
        /* width: 100%; */
        padding: 5px;
        border-radius: 3px;
        border: 1px solid #ccc;
    }
    .content-container textarea {
        width: 100%;
        height: 100px;
        padding: 5px;
        border-radius: 3px;
        border: 1px solid #ccc;
    }
</style>