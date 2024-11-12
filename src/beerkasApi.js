import axios from "axios";

export function getCsrfToken() {
    return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}

export async function getBerkasesList(row) {
    try {
        const response = await axios.get(`/api/berkasesList`, {
            params: { id: row.id },
        });
        const berkasesList = response.data.berkasesList;
        console.log("berkasesList", berkasesList);
        return berkasesList;
    } catch (error) {
        console.error("Error fetching berkases list:", error);
        throw error;
    }
}

export async function getBerkases(row, jenis) {
    try {
        const response = await axios.get(`/api/berkases`, {
            params: { id: row.id, jenis },
        });
        const ret = response.data;
        // const ret = {
        //     berkases: response.data.berkases,
        //     revision: response.data.revision,
        //     berkas_revision: response.data.berkas_revision
        // }
        console.log("berkases", response);
        return ret;
    } catch (error) {
        console.error("Error fetching berkases:", error);
        throw error;
    }
}

export async function getBerkas(id) {
    try {
        const response = await axios.get(`/api/berkas`, { params: { id } });
        const ret = response.data;
        // const ret = {
        //     berkas: response.data.berkas,
        //     berkas_revision: response.data.berkas_revision
        // }
        console.log("berkas", response);
        return ret;
    } catch (error) {
        console.error("Error fetching berkas:", error);
        throw error;
    }
}

export async function addBerkas(row, jenis, file) {
    try {
        const formData = new FormData();
        formData.append("id", row.id);
        formData.append("jenis", jenis);
        formData.append("file", file);

        const csrfToken = getCsrfToken();
        const response = await axios.post("/api/berkas/add", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
                "X-CSRFToken": csrfToken,
            },
        });

        if (response.data.status === 200) {
            console.log("Berkas added successfully");
            return response.data;
        } else {
            console.error("Failed to add berkas");
            response.data = {
              status: 400,
              message: "Failed to set nilai status",
            };
            return response.data;
        }
    } catch (error) {
        console.error("Error adding berkas:", error);
        throw error;
    }
}

export async function komentarBerkas(berkas, komentar) {
    try {
        const csrfToken = getCsrfToken();

        const response = await axios.post(
          "/api/berkas/komen",
          {
            id: berkas.id,
            komentar,
          },
          {
            headers: {
              "Content-Type": "multipart/form-data",
              "X-CSRFToken": csrfToken,
            },
          }
        );

        if (response.data.status === 200) {
            console.log("Komentar added successfully");
            return response.data;
        } else {
            console.error("Failed to add komentar");
            response.data = {
              status: 400,
              message: "Failed to set nilai status",
            };
            return response.data;
        }
    } catch (error) {
        console.error("Error adding komentar:", error);
        throw error;
    }
}

export async function getPendaftaran(id) {
    try {
        const response = await axios.get(`/api/pendaftaran`, { params: { id } });
        const ret = response.data;
        console.log("pendaftaran", response);
        return ret;
    } catch (error) {
        console.error("Error fetching pendaftaran:", error);
        throw error;
    }
}

export async function setNilaiStatus(id, data) {
    try {
        const csrfToken = getCsrfToken();

        const response = await axios.post(
            `/api/pendaftaran/set-nilai/${id}`,
            {
                ...data,
            },
            {
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
            }
        );

        if (response.data.status === 200) {
            console.log("Nilai status set successfully");
            return response.data;
        } else {
            console.error("Failed to set nilai status");
            response.data = {
                status: 400,
                message: "Failed to set nilai status",
            };
            return response.data;
        }
    } catch (error) {
        console.error("Error setting nilai status:", error);
        throw error;
    }
}

export async function nextStatus(id, data) {
    try {
        const formData = new FormData();
        formData.append("id", id);
        if (data) {
            formData.append("data", JSON.stringify(data));
        }

        const csrfToken = getCsrfToken();

        const response = await axios.post(
            `/api/pendaftaran/next-status`,
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": csrfToken,
                },
            }
        );

        if (response.data.status === 200) {
            console.log("Status updated successfully");
            return response.data;
        } else {
            console.error("Failed to update status");
            response.data = {
              status: 400,
              message: "Failed to set nilai status",
            };
            return response.data;
        }
    } catch (error) {
        console.error("Error updating status:", error);
        throw error;
    }
}

export async function deletePendaftaran(id) {
    try {
        const formData = new FormData();
        formData.append("id", id);

        const csrfToken = getCsrfToken();

        const response = await axios.post(
            `/api/pendaftaran/delete`,
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": csrfToken,
                },
            }
        );

        if (response.data.status === 200) {
            console.log("Pendaftaran deleted successfully");
            return response.data;
        } else {
            console.error("Failed to delete pendaftaran");
            response.data = {
                status: 400,
                message: "Failed to delete pendaftaran",
            };
            return response.data;
        }
    } catch (error) {
        console.error("Error deleting pendaftaran:", error);
        throw error;
    }
}