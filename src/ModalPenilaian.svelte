<script>
  import { getPendaftaran, nextStatus, setNilaiStatus } from "@/beerkasApi";

    export let isOpen = false;
    export let user = {};
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
        // inputTesPemahaman = pendaftaran?.nilai_tp ?? { pm: 0, km: 0, pa: 0, kmp: 0, sp: 0, komentar: "" }; // selection_status 3
        // inputWawancaraAsisten = pendaftaran?.nilai_wa ?? { pd: 0, rrd: 0, mdb: 0, komentar: "" }; // selection_status 4
        // inputWawancaraDosen = pendaftaran?.nilai_wd ?? { pd: 0, rrd: 0, mdb: 0, komentar: "" }; // selection_status 5
        
        // force structure
        inputTesMicroteaching = {
            pm: pendaftaran?.nilai_tm?.pm ?? 0,
            km: pendaftaran?.nilai_tm?.km ?? 0,
            pa: pendaftaran?.nilai_tm?.pa ?? 0,
            kmp: pendaftaran?.nilai_tm?.kmp ?? 0,
            sp: pendaftaran?.nilai_tm?.sp ?? 0,
            komentar: pendaftaran?.nilai_tm?.komentar ?? ""
        };

        inputTesPemahaman = {
            nilai: pendaftaran?.nilai_tp?.nilai ?? 0,
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
                rows[rows.findIndex(row=>row.id==pendaftaran.id)] = newPendaftaran.pendaftaran;
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
                rows[rows.findIndex(row=>row.id==pendaftaran.id)] = newPendaftaran.pendaftaran;
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
                    {:else}
                    <div>
                        Belum ada penilaian
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
                        <!-- <h2>Tes Microteaching</h2> -->
                        <label></label>
                        <label>Skala Nilai: 1 - 100</label>
                            <label>Penguasaan Materi: <input type="number" min="1" max="100" bind:value={inputTesMicroteaching.pm} readonly={!user.is_superuser || selection_status !== 2} on:input={(e) => handleInputChange(e, 'pm', 'microteaching')} /></label>
                            <label>Kemampuan Menjelaskan: <input type="number" min="1" max="100" bind:value={inputTesMicroteaching.km} readonly={!user.is_superuser || selection_status !== 2} on:input={(e) => handleInputChange(e, 'km', 'microteaching')} /></label>
                            <label>Penguasaan Audience: <input type="number" min="1" max="100" bind:value={inputTesMicroteaching.pa} readonly={!user.is_superuser || selection_status !== 2} on:input={(e) => handleInputChange(e, 'pa', 'microteaching')} /></label>
                            <label>Kemampuan Menjawab Pertanyaan: <input type="number" min="1" max="100" bind:value={inputTesMicroteaching.kmp} readonly={!user.is_superuser || selection_status !== 2} on:input={(e) => handleInputChange(e, 'kmp', 'microteaching')} /></label>
                            <label>Sikap Presentasi: <input type="number" min="1" max="100" bind:value={inputTesMicroteaching.sp} readonly={!user.is_superuser || selection_status !== 2} on:input={(e) => handleInputChange(e, 'sp', 'microteaching')} /></label>
                            <label>Komentar: <textarea bind:value={inputTesMicroteaching.komentar} readonly={!user.is_superuser || selection_status !== 2} on:input={(e) => handleInputChange(e, 'komentar', 'microteaching')}></textarea></label>
                        {#if user.koordinator && selection_status === 2}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Lanjut</button>
                        </div>
                        {:else}
                        <div>
                            (diisi oleh koordinator asisten)
                        </div>
                        {/if}
                    {/if}

                    {#if selectedStatus === 3}
                        <!-- <h2>Tes Pemahaman</h2> -->
                        <label></label>
                        <label>Skala Nilai: 1 - 100</label>
                           <label>Nilai: <input type="number" min="1" max="100" bind:value={inputTesPemahaman.nilai} readonly={!user.is_superuser || selection_status !== 3} on:input={(e) => handleInputChange(e, 'nilai', 'pemahaman')} /></label>
                            <label>Komentar: <textarea bind:value={inputTesPemahaman.komentar} readonly={!user.is_superuser || selection_status !== 3} on:input={(e) => handleInputChange(e, 'komentar', 'pemahaman')}></textarea></label>
                        {#if user.koordinator && selection_status === 3}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Lanjut</button>
                        </div>
                        {:else}
                        <div>
                            (diisi oleh koordinator asisten)
                        </div>
                        {/if}
                    {/if}

                    {#if selectedStatus === 4}
                        <!-- <h2>Wawancara Asisten</h2> -->
                        <label></label>
                        <label>Skala Nilai: 1 - 5</label>
                        <label>Pengenalan Diri: <input type="number" min="1" max="5" bind:value={inputWawancaraAsisten.pd} readonly={!user.is_superuser || selection_status !== 4} on:input={(e) => handleInputChange(e, 'pd', 'wawancaraAsisten')} /></label>
                        <label>Rencana dan Rancangan ke Depan: <input type="number" min="1" max="5" bind:value={inputWawancaraAsisten.rrd} readonly={!user.is_superuser || selection_status !== 4} on:input={(e) => handleInputChange(e, 'rrd', 'wawancaraAsisten')} /></label>
                        <label>Motivasi dalam Bekerja: <input type="number" min="1" max="5" bind:value={inputWawancaraAsisten.mdb} readonly={!user.is_superuser || selection_status !== 4} on:input={(e) => handleInputChange(e, 'mdb', 'wawancaraAsisten')} /></label>
                        <label>Komentar: <textarea bind:value={inputWawancaraAsisten.komentar} readonly={!user.is_superuser || selection_status !== 4} on:input={(e) => handleInputChange(e, 'komentar', 'wawancaraAsisten')}></textarea></label>
                        {#if user.koordinator && selection_status === 4}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Lanjut</button>
                        </div>
                        {:else}
                        <div>
                            (diisi oleh koordinator asisten)
                        </div>
                        {/if}
                    {/if}
                    {#if selectedStatus === 5}
                        <!-- <h2>Wawancara Dosen</h2> -->
                        <label></label>
                        <label>Skala Nilai: 1 - 5</label>
                        <label>Pengenalan Diri: <input type="number" min="1" max="5" bind:value={inputWawancaraDosen.pd} readonly={!user.is_superuser || selection_status !== 5} on:input={(e) => handleInputChange(e, 'pd', 'wawancaraDosen')} /></label>
                        <label>Rencana dan Rancangan ke Depan: <input type="number" min="1" max="5" bind:value={inputWawancaraDosen.rrd} readonly={!user.is_superuser || selection_status !== 5} on:input={(e) => handleInputChange(e, 'rrd', 'wawancaraDosen')} /></label>
                        <label>Motivasi dalam Bekerja: <input type="number" min="1" max="5" bind:value={inputWawancaraDosen.mdb} readonly={!user.is_superuser || selection_status !== 5} on:input={(e) => handleInputChange(e, 'mdb', 'wawancaraDosen')} /></label>
                        <label>Komentar: <textarea bind:value={inputWawancaraDosen.komentar} readonly={!user.is_superuser || selection_status !== 5} on:input={(e) => handleInputChange(e, 'komentar', 'wawancaraDosen')}></textarea></label>
                        {#if user.koordinator && selection_status === 5}
                        <div>
                            <button on:click={handleSimpan}>Simpan</button>
                            <button on:click={handleLanjut}>Terima</button>
                        </div>
                        {:else}
                        <div>
                            (diisi oleh dosen yang bersangkuktan)
                        </div>
                        {/if}
                    {/if}
                </div>
            </div>
        </dialog>
    </div>
{/if}

<style>
    /* CSS Variables */
    :root {
        --modal-bg: white;
        --modal-padding: 2rem;
        --border-radius: 8px;
        --primary-color: #007bff;
        --dark-color: #2b2928;
        --border-color: #ccc;
    }

    /* Layout Components */
    .overlay {
        position: fixed;
        inset: 0; /* shorthand for top/right/bottom/left: 0 */
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal {
        background: var(--modal-bg);
        padding: var(--modal-padding);
        border-radius: var(--border-radius);
        width: 30vw;
        height: 60vh;
        max-width: 90%;
        max-height: 90%;
        display: flex;
        flex-direction: column;
    }

    /* Header Styles */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        margin-bottom: 1rem;
    }

    .header {
        flex: 1;
        padding-bottom: 5px;
        font-size: 26px;
        font-weight: bold;
        border-bottom: 3px solid black;
    }

    .header-container h1 {
        margin: 0;
        font-size: larger;
    }

    /* Close Button */
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

    /* Content Layout */
    .body-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 1;
        overflow-y: auto;
    }

    .content-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* Navigation Chips */
    .jenis-container {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        width: 100%;
        gap: 5px;
        margin-bottom: 1rem;
    }

    .jenis-chip {
        width: 130px;
        background-color: var(--dark-color);
        cursor: pointer;
        color: white;
        padding: 10px;
        border-radius: var(--border-radius);
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .jenis-chip.selected {
        border: 1px solid var(--primary-color);
    }

    /* Form Elements */
    .content-container label {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 1.2rem;
        width: 100%;
        font-weight: 500;
        color: #333;
    }

    .content-container label:first-child {
        margin-top: 0.5rem;
    }

    .content-container input {
        margin-top: 0.3rem;
        padding: 8px 12px;
        border-radius: 4px;
        border: 1px solid var(--border-color);
        width: 60%;
        font-size: 0.95rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }

    .content-container input:focus {
        outline: none;
        border-color: var(--primary-color);B
        box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
    }

    .content-container input:hover:not(:focus) {
        border-color: #999;
    }

    .content-container input[type="number"] {
        -moz-appearance: textfield;
    }

    .content-container input[type="number"]::-webkit-outer-spin-button,
    .content-container input[type="number"]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    .content-container textarea {
        margin-top: 0.3rem;
        width: 80%;
        height: 100px;
        padding: 8px 12px;
        border-radius: 4px;
        border: 1px solid var(--border-color);
        resize: vertical;
        font-size: 0.95rem;
        font-family: inherit;
        transition: border-color 0.2s, box-shadow 0.2s;
    }

    .content-container textarea:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
    }

    .content-container textarea:hover:not(:focus) {
        border-color: #999;
    }

    /* Update header scale */
    .content-container label:has(+ label:first-of-type) {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }

    /* Grid Layout for Form */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        width: 100%;
        padding: 1rem;
    }

    /* Buttons */
    .modal button {
        margin-top: 0;
        padding: 0.5rem 1rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        cursor: pointer;
    }

    /* Media Queries */
    @media (max-width: 768px) {
        .modal {
            width: 90vw;
        }

        .grid-container {
            grid-template-columns: 1fr;
        }
    }
</style>