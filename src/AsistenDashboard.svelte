<!-- src/Pagination.svelte -->
<script>
    import {string_to_pdf} from './pdf-utils'
    import axios from 'axios';

    let ticker = 1;

    // context props
    export let user = {};
    export let rows = [];
    export let praktikum_options = [];
    export let periode_options = [];
    // table props
    export let itemsPerPage = "10";

    // filter vars
    let selectedPraktikum = '';
    let selectedPeriode = '';
    let selectedNama = '';
    
    let currentPage = 1;
    let totalPages = Math.ceil(rows.length / itemsPerPage);

    let sort_by = 'nama';
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
        if (selectedPeriode) {
            afilteredRows = afilteredRows.filter(row => row.periode === String(selectedPeriode));
        }
        if (selectedPraktikum) {
            afilteredRows = afilteredRows.filter(row => row.nama_praktikum === (selectedPraktikum));
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

    async function generatePDF() {
        const params = {
            periode: selectedPeriode,
            praktikum: selectedPraktikum,
            sort_by,
            order
        }
        const response = await axios.get('/api/asisten/pdf', {params});
        console.log(response.data);
        const html_string = response.data?.html_string;
        string_to_pdf(html_string, {}, response.data?.file_name);
    }

</script>

<div class="filter">
<div class="filter-nama">
    <label for="nama">Nama/NIM:</label>
    <input type="text" id="nama" bind:value={selectedNama} placeholder="Cari Nama/NIM">
</div>
<div class="filter-praktikum">
    <label for="praktikum">Praktikum:</label>
    <select name="praktikum" id="praktikum" bind:value={selectedPraktikum}>
        <option value="">--Pilih Praktikum--</option>
        {#each praktikum_options as praktikum}
            <option value={praktikum.label}>{praktikum.label}</option>
        {/each}
    </select>
</div>
<div class="filter-periode">  
    <label for="periode">Periode:</label>
    <select name="periode" id="periode" bind:value={selectedPeriode}>
        <option value="">--Pilih Periode--</option>
        {#each periode_options as year}
            <option value={year}>{year}</option>
        {/each}
    </select>
</div>

<div class="filter-reset">
    <button on:click={() => {
        selectedPeriode = '';
        selectedPraktikum = '';
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
                <th style="width: 140px;">
                    <a href="javascript:void(0)" on:click={() => sortTable('nim')}>
                        NIM {sort_by === 'nim' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
                <th >
                    <a href="javascript:void(0)" on:click={() => sortTable('nama')}>
                        Nama {sort_by === 'nama' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
                <th style="width: 400px;">
                    <a href="javascript:void(0)" on:click={() => sortTable('praktikum')}>
                        Asisten {sort_by === 'praktikum' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
            <th style="width: 200px;">
                <a href="javascript:void(0)" on:click={() => sortTable('periode')}>
                    Periode {sort_by === 'periode' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
        </tr>
    </thead>
    <tbody>
        {#each filteredRows as row}
            <tr>
                    <td>{row.nim}</td>
                    <td>{row.nama}</td>
                    <td>{row.nama_praktikum}</td>
                    <td>{row.periode}</td>
            </tr>
        {:else}
            <tr>
                <td colspan="4">
                    Belum ada Asisten.
                </td>
            </tr>
        {/each}
        {#if rows.length > itemsPerPage}
            <tr>
                <td colspan="4">
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
