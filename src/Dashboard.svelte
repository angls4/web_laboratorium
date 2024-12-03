<!-- src/Dashboard.svelte -->
<script>
    import {string_to_pdf} from './pdf-utils'
    import ModalBerkas from './ModalBerkas.svelte';
    import axios from 'axios';
    import {deletePendaftaran, getBerkasesList, getPendaftaran, nextStatus} from '@/beerkasApi';
  import ModalPenilaian from './ModalPenilaian.svelte';

    let modalBerkas;

    let ticker = 1;

    // context props
    export let user = {};
    export let rows = [];
    export let tahun_options = [];
    export let nilai_options = [];
    export let status_options = [];
    // table props
    export let itemsPerPage = "10";

    // filter vars
    let selectedTahun = '';
    let selectedNilai = '';
    let selectedStatus = '';
    let selectedNama = '';
    let selectedPendaftaran = {};
    let selectedBerkasesList = [];

    
    let currentPage = 1;
    let totalPages = Math.ceil(rows.length / itemsPerPage);

    let sort_by = 'uploaded_at';
    let order = 'desc';
    function sortTable(column) {
        if (sort_by === column) {
            order = order === 'asc' ? 'desc' : 'asc';
        } else {
            sort_by = column;
            order = 'asc';
        }
        rows = rows.sort((a, b) => {
            if (order === 'asc') {
                return a[sort_by] > b[sort_by] ? 1 : -1;
            } else {
                return a[sort_by] < b[sort_by] ? 1 : -1;
            }
        });
    }
    let filteredRows = rows;

    $: {
        let afilteredRows = rows;
        let a = itemsPerPage
        if (selectedTahun) {
            afilteredRows = afilteredRows.filter(row => row.tahun === selectedTahun);
        }
        if (selectedNilai) {
            afilteredRows = afilteredRows.filter(row => row.nilai_id === selectedNilai);
        }
        if (selectedStatus) {
            afilteredRows = afilteredRows.filter(row => row.status_id === Number(selectedStatus));
        }
        if (selectedNama) {
            afilteredRows = afilteredRows.filter(row => row.nama.toLowerCase().includes(selectedNama.toLowerCase()) || row.nim.toLowerCase().includes(selectedNama.toLowerCase()));
        }
        totalPages = Math.ceil(afilteredRows.length / Number(itemsPerPage));
        console.log('totalPages', totalPages);
        console.log('itemsPerPage', itemsPerPage);
        const start = (currentPage - 1) * Number(itemsPerPage);
        const end = start + Number(itemsPerPage);
        console.log('afilteredRows', afilteredRows);
        console.log('start', start);
        console.log('end', end);
        afilteredRows = afilteredRows.slice(start, end);
        filteredRows = afilteredRows
    }


    function changePage(newPage) {
        if (newPage >= 1 && newPage <= totalPages) {
            currentPage = newPage;
        }
    }

    function closeBerkasModal() {
        if (modalBerkas)
            modalBerkas.closeBerkasModal();
        else
            console.log('modalBerkas is not defined');
    }
    async function openBerkasModal(pendaftaran) {
        if (selectedPendaftaran.id !== pendaftaran.id)
            modalBerkas.changePendaftaran(pendaftaran, await getBerkasesList(pendaftaran));
        if (modalBerkas)
            modalBerkas.openModal();
        else
            console.log('modalBerkas is not defined');
    }

    async function generatePDF() {
        const params = {
            tahun: selectedTahun,
            nilai: selectedNilai,
            status: selectedStatus,
            sort_by,
            order
        }
        const response = await axios.get('/api/pendaftaran/pdf', {params});
        const html_string = response.data?.html_string;
        const options = user.asisten ? { width: "1800px", orientation: "landscape" } : {};
        string_to_pdf(html_string, options, response.data?.file_name);
    }
    let penilaianModal;
    async function openPenilaianModal(pendaftaran) {
        penilaianModal.changePendaftaran(pendaftaran);
        if (penilaianModal) {
            penilaianModal.openModal();
        } else {
            console.log('penilaianModal is not defined');
        }
    }
    let fetching = false
    async function handleLanjut(pendaftaran) {
        if (fetching) return;
        try {
            fetching = true;
            const res = await nextStatus(pendaftaran.id);
            if (res && res.status == 200) {
                alert('Berhasil melanjutkan ke status berikutnya');
                const newPendaftaran = await getPendaftaran(pendaftaran.id);
                rows[rows.findIndex(row=>row.id==pendaftaran.id)] = newPendaftaran.pendaftaran;
            } else {
                alert('Gagal melanjutkan ke status berikutnya');
            }
        } catch (error) {
            console.error('Error during handleLanjut:', error);
            alert('Terjadi kesalahan saat melanjutkan ke status berikutnya');
        }
        fetching = false;
    }
    async function handleDelete(pendaftaran) {
        if (fetching) return;
        if (confirm('Apakah Anda yakin ingin menghapus pendaftaran ini?')) {
            try {
                fetching = true;
                const res = await deletePendaftaran(pendaftaran.id);
                if (res && res.status == 200) {
                    alert('Berhasil menghapus pendaftaran');
                    rows = rows.filter(row => row.id !== pendaftaran.id);
                } else {
                    alert('Gagal menghapus pendaftaran');
                }
            } catch (error) {
                console.error('Error during handleDelete:', error);
                alert('Terjadi kesalahan saat menghapus pendaftaran');
            }
            fetching = false;
        }
    }

</script>
<ModalBerkas bind:rows={rows} bind:user={user} bind:ticker={ticker} bind:this={modalBerkas} bind:pendaftaran={selectedPendaftaran} bind:berkasesList={selectedBerkasesList}>
    <div slot="header">
        <h1>Berkas-Berkas Pendaftaran</h1>
    </div>
</ModalBerkas>
<ModalPenilaian bind:user={user} bind:this={penilaianModal} bind:rows={rows}></ModalPenilaian>


<div class="filter">
<div class="filter-nama">
    <label for="nama">Nama/NIM:</label>
    <input type="text" id="nama" bind:value={selectedNama} placeholder="Cari Nama/NIM">
</div>
<div class="filter-tahun">  
    <label for="tahun">Tahun:</label>
    <select name="tahun" id="tahun" bind:value={selectedTahun}>
        <option value="">--Pilih Tahun--</option>
        {#each tahun_options as year}
            <option value={year}>{year}</option>
        {/each}
    </select>
</div>

<div class="filter-nilai">
    <label for="nilai">Nilai:</label>
    <select name="nilai" id="nilai" bind:value={selectedNilai}>
        <option value="">--Pilih Nilai--</option>
        {#each nilai_options as nilai}
            <option value={nilai.value}>{nilai.label}</option>
        {/each}
    </select>
</div>

<div class="filter-status">
    <label for="status">Status:</label>
    <select name="status" id="status" bind:value={selectedStatus}>
        <option value="">--Pilih Status--</option>
        {#each status_options as status}
            <option value={status.value}>{status.label}</option>
        {/each}
    </select>
</div>
<div class="filter-reset">
    <button on:click={() => {
        selectedTahun = '';
        selectedNilai = '';
        selectedStatus = '';
        selectedNama = '';
        currentPage = 1;
    }}>
        Reset Filter
    </button>
</div>
<div>
    <button class="generate-pdf" on:click={generatePDF}>Download PDF</button>
</div>
</div>
<div class="table-container">
<table class="dashboard-table">
    <thead>
        <tr class="table-head">
            {#if user.asisten}
                <th style="width: 100px;">
                    <a href="javascript:void(0)" on:click={() => sortTable('nim')}>
                        NIM {sort_by === 'nim' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
                <th style="width: 200px;">
                    <a href="javascript:void(0)" on:click={() => sortTable('nama')}>
                        Nama {sort_by === 'nama' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
                <th style="width: 100px;">Sosial Media</th>
            {/if}
            <th style="width: 200px;">Berkas</th>
            {#if !user.asisten}
                <th>
                    <a href="javascript:void(0)" on:click={() => sortTable('praktikum')}>
                        Praktikum {sort_by === 'praktikum' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
            {/if}
            <th style="width: 90px;">
                <a href="javascript:void(0)" on:click={() => sortTable('uploaded_at')}>
                    Tanggal {sort_by === 'uploaded_at' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th style="width: 90px;">Tanggal Edit</th>
            <th style="width: 50px;">
                <a href="javascript:void(0)" on:click={() => sortTable('ipk')}>
                    IPK {sort_by === 'ipk' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th style="width: 80px;">
                <a href="javascript:void(0)" on:click={() => sortTable('nilai')}>
                    Nilai Praktikum {sort_by === 'nilai' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <!-- <th>
                <a href="javascript:void(0)" on:click={() => sortTable('nilai_tm')}>
                    Nilai TM {sort_by === 'nilai_tm' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th>
                <a href="javascript:void(0)" on:click={() => sortTable('nilai_tp')}>
                    Nilai TP {sort_by === 'nilai_tp' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th>
                <a href="javascript:void(0)" on:click={() => sortTable('nilai_wa')}>
                    Nilai WA {sort_by === 'nilai_wa' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th>
                <a href="javascript:void(0)" on:click={() => sortTable('nilai_wd')}>
                    Nilai WD {sort_by === 'nilai_wd' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th> -->
            <th >Status</th>
            {#if user.jabatan !== 'Asisten'}
                <th style="width: 120px;">Actions</th>
            {/if}
        </tr>
    </thead>
    <tbody>
        {#each filteredRows as row}
            <tr>
                {#if user.asisten}
                    <td>{row.nim}</td>
                    <td>{row.nama}</td>
                    <td>
                        <p><a href={row.linkedin} target="_blank">LinkedIn</a></p>
                        <p><a href={row.instagram} target="_blank">Instagram</a></p>
                    </td>
                {/if}
                <!-- <td><a href={"aa"} target="_blank" download>Download</a></td> -->
                <td>
                    <button on:click={()=>openBerkasModal(row)}>Lihat Semua Berkas</button>
                    {#if row.berkas_revision.unrevised}
                    <p>{row.berkas_revision.revised}/{row.berkas_revision.unrevised + row.berkas_revision.revised} revisi selesai</p>
                    {:else}
                    <!-- <p>Belum ada revisi</p> -->
                    {/if}
                    <!-- <a on:click={()=>getBerkasesList(row)}>test getBerkasesList</a> -->
                </td>
                {#if !user.asisten}
                    <td>{row.praktikum}</td>
                {/if}
                <td>{row.uploaded_at}</td>
                <td>{row.edited_at}</td>
                <td>{row.ipk}</td>
                <td>{row.nilai}</td>
                <!-- <td>{user.koordinator ? row.form.as_p : row.get_selection_status_display}</td> -->
                <!-- <td>{row.nilai_tm ?? "-"}</td>
                <td>{row.nilai_tp ?? "-"}</td>
                <td>{row.nilai_wa ?? "-"}</td>
                <td>{row.nilai_wd ?? "-"}</td> -->
                <td>
                    <p>{row.status}</p>
                    <p>
                        {#if row.status_id == 1}
                            {#if user.koordinator}
                                {#if row.berkas_revision.unrevised == 0}
                                    <button on:click={()=>handleLanjut(row)}>Ke Tahap Berikutnya</button>
                                {:else}
                                    <button on:click={()=>openBerkasModal(row)}>Berkas Perlu Direvisi</button>
                                {/if}
                            {:else}
                                {#if row.berkas_revision.unrevised > 0}
                                    <p style="margin-top: 5px; font-style:italic">(Berkas Perlu Direvisi)</p>
                                {/if}
                            {/if}
                        {:else if user.asisten}
                            <button on:click={()=>openPenilaianModal(row)}>
                                Tinjau Nilai
                            </button>
                        {/if}
                        {#if row.status_id === 6}
                            <!-- <p> -->
                                <a href={`/send-loa/${row.id}`} target="_blank"><button>Kirim LOA</button></a>
                            <!-- </p> -->
                        {/if}
                    </p>
                    <!-- <p>
                        <input type="number">
                        <button on:click={() => openBerkasModal(row)}>Submit</button>
                    </p> -->
                </td>
                {#if user.jabatan !== 'Asisten'}
                    <td>
                        <p>
                            <a href={`/pendaftaran/${row.id}`}><button>Edit</button></a>
                            {#if user.koordinator}
                                <a on:click={()=>handleDelete(row)}><button>Delete</button></a>
                                
                            {/if}
                        </p>
                        <!-- <p>
                            <a on:click={()=>openPenilaianModal(row)}><button>Nilai</button></a>
                        </p> -->
                    </td>
                {/if}
            </tr>
        {:else}
            <tr>
                <td colspan={user.asisten ? 10 : 8}>
                    Belum ada pendaftaran. Daftar <a href="/pendaftaran">di sini</a>.
                </td>
            </tr>
        {/each}
        {#if rows.length > itemsPerPage}
            <tr>
                <td colspan={user.asisten ? 10 : 8}>
                    <p>Showing {currentPage === totalPages ? filteredRows.length : currentPage * itemsPerPage} of {rows.length} entries</p>
                </td>
            </tr>
        {/if}
    </tbody>
</table>

<div class="pagination-controls">
    <button on:click={() => changePage(currentPage - 1)} disabled={currentPage === 1}>
        Previous
    </button>
    <span>Page {currentPage} of {totalPages == 0 ? 1 : totalPages}</span>
    <button on:click={() => changePage(currentPage + 1)} disabled={currentPage === totalPages}>
        Next
    </button>
</div>

<div class="items-per-page">
    <label for="itemsPerPage">Items per page:</label>
    <select id="itemsPerPage" bind:value={itemsPerPage} on:change={() => { currentPage = 1; totalPages = Math.ceil(filteredRows.length / itemsPerPage); }}>
        <option value=1>1</option>
        <option value=5>5</option>
        <option value=10>10</option>
        <option value="20">20</option>
    </select>
</div>
</div>

<style>
    .pagination-controls {
        margin: 10px 0px;
        display: flex;
        gap: 1rem;
        align-items: center;
        justify-content: center;
    }
    .pagination-controls button {
        margin:0;
        padding: 0.5rem 1rem;
        font-size: medium;
        cursor: pointer;
    }
    .items-per-page {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 10px 0;
        margin-bottom: 40px;
    }
    .items-per-page label {
        font-weight: bold;
    }
    .items-per-page select {
        padding: 0.5rem;
        font-size: medium;
    }
</style>
