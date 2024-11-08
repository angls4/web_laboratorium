import Pagination from "@/Pagination.svelte";
import { mount } from "svelte";

// window.alert("Hello from Svelte!");
// console.log(window.fullData);

mount(Pagination, {
  target: document.getElementById("svelte-table"),
  props: {
    ...window.context,
    itemsPerPage: 10,
  },
});

