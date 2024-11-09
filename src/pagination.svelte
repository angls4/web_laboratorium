<!-- src/Pagination.svelte -->
<script>
  import axios from 'axios';
    import {string_to_pdf} from './pdf-utils'
    // context props
    export let user = {};
    export let rows = [];
    export let tahun_options = [];
    export let nilai_options = [];
    export let status_options = [];
    // table props
    export let itemsPerPage = 10;

    // filter vars
    let selectedTahun = '';
    let selectedNilai = '';
    let selectedStatus = '';

    
    let currentPage = 1;
    let totalPages = Math.ceil(rows.length / itemsPerPage);

    let sort_by = '';
    let order = 'asc';
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

    function getFilteredRows() {
        let filteredRows = rows;
        if (selectedTahun) {
            filteredRows = filteredRows.filter(row => row.tahun === selectedTahun);
        }
        if (selectedNilai) {
            filteredRows = filteredRows.filter(row => row.nilai_id === selectedNilai);
        }
        if (selectedStatus) {
            filteredRows = filteredRows.filter(row => row.status_id === Number(selectedStatus));
        }
        totalPages = Math.ceil(filteredRows.length / Number(itemsPerPage));
        const start = (currentPage - 1) * Number(itemsPerPage);
        const end = start + Number(itemsPerPage);
        console.log('filteredRows', filteredRows);
        console.log('start', start);
        console.log('end', end);
        filteredRows = filteredRows.slice(start, end);
        return filteredRows;
    }


    function changePage(newPage) {
        if (newPage >= 1 && newPage <= totalPages) {
            currentPage = newPage;
        }
    }   

    async function generatePDF() {
        const params = {
            tahun: selectedTahun,
            nilai: selectedNilai,
            status: selectedStatus,
            sort_by,
            order
        }
        const response = await axios.get('api/pendaftaran/pdf', {params});
        const html_string = response.data?.html_string;
        const options = user.asisten ? { width: "1800px", orientation: "landscape" } : {};
        string_to_pdf(html_string, options);
    }

</script>

<div class="filter">
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
</div>
<div class="table-container">
<table class="dashboard-table">
    <thead>
        <tr class="table-head">
            {#if user.asisten}
                <th>
                    <a href="javascript:void(0)" on:click={() => sortTable('nim')}>
                        NIM {sort_by === 'nim' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
                <th>
                    <a href="javascript:void(0)" on:click={() => sortTable('nama')}>
                        Nama {sort_by === 'nama' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
                <th>Sosial Media</th>
            {/if}
            <th>File</th>
            {#if !user.asisten}
                <th>
                    <a href="javascript:void(0)" on:click={() => sortTable('praktikum')}>
                        Praktikum {sort_by === 'praktikum' ? (order === 'desc' ? '▼' : '▲') : ''}
                    </a>
                </th>
            {/if}
            <th>
                <a href="javascript:void(0)" on:click={() => sortTable('uploaded_at')}>
                    Tanggal {sort_by === 'uploaded_at' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th>Tanggal Edit</th>
            <th>
                <a href="javascript:void(0)" on:click={() => sortTable('ipk')}>
                    IPK {sort_by === 'ipk' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th>
                <a href="javascript:void(0)" on:click={() => sortTable('nilai')}>
                    Nilai Praktikum {sort_by === 'nilai' ? (order === 'desc' ? '▼' : '▲') : ''}
                </a>
            </th>
            <th>Status</th>
            {#if user.jabatan !== 'Asisten'}
                <th>Actions</th>
            {/if}
        </tr>
    </thead>
    <tbody>
        {#each getFilteredRows() as row}
            <tr>
                {#if user.asisten}
                    <td>{row.nim}</td>
                    <td>{row.nama}</td>
                    <td>
                        <p><a href={row.linkedin} target="_blank">LinkedIn</a></p>
                        <p><a href={row.instagram} target="_blank">Instagram</a></p>
                    </td>
                {/if}
                <td><a href={row.file} target="_blank" download>Download</a></td>
                {#if !user.asisten}
                    <td>{row.praktikum}</td>
                {/if}
                <td>{row.uploaded_at}</td>
                <td>{row.edited_at}</td>
                <td>{row.ipk}</td>
                <td>{row.nilai}</td>
                <!-- <td>{user.koordinator ? row.form.as_p : row.get_selection_status_display}</td> -->
                <td>{row.status}</td>
                {#if user.jabatan !== 'Asisten'}
                    <td>
                        <div>
                            <a href={`/edit_pendaftaran/${row.id}`}>Edit</a>
                            {#if user.koordinator}
                                <a href={`/delete_pendaftaran/${row.id}`}>Delete</a>
                                {#if row.status === 6}
                                    <p>
                                        <a href={`/send_loa/${row.id}`} target="_blank">Kirim LOA</a>
                                    </p>
                                {/if}
                            {/if}
                        </div>
                    </td>
                {/if}
            </tr>
        {:else}
            <tr>
                <td colspan={user.asisten ? 10 : 6}>
                    Belum ada pendaftaran. Daftar <a href="/pendaftaran">di sini</a>.
                </td>
            </tr>
        {/each}
        {#if rows.length > itemsPerPage}
            <tr>
                <td colspan={user.asisten ? 10 : 6}>
                    <p>Showing {currentPage === totalPages ? rows.length : currentPage * itemsPerPage} of {rows.length} entries</p>
                </td>
            </tr>
        {/if}
    </tbody>
</table>

<div class="pagination-controls">
    <button on:click={() => changePage(currentPage - 1)} disabled={currentPage === 1}>
        Previous
    </button>
    <span>Page {currentPage} of {totalPages}</span>
    <button on:click={() => changePage(currentPage + 1)} disabled={currentPage === totalPages}>
        Next
    </button>
</div>

<div class="items-per-page">
    <label for="itemsPerPage">Items per page:</label>
    <select id="itemsPerPage" bind:value={itemsPerPage} on:change={() => { currentPage = 1; totalPages = Math.ceil(rows.length / itemsPerPage); }}>
        <option value=1>1</option>
        <option value=5>5</option>
        <option value=10>10</option>
        <option value="20">20</option>
    </select>
</div>
 <button class="button" on:click={generatePDF}>Generate PDF</button>
</div>


<style>
    .pagination-controls {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    .items-per-page {
        margin-top: 1rem;
    }
</style>
