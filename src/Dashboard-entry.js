import Dashboard from "./Dashboard.svelte";
import { mount } from "svelte";

// window.alert("Hello from Svelte!");
// console.log(window.fullData);

mount(Dashboard, {
  target: document.getElementById("svelte-table"),
  props: {
    ...window.context,
  },
});


const jsonTesMicroteaching = {
  nilai: 100, // 1-100
  komentar: "Bagus",
}

const jsonTesPemahaman = {
  pm: 100, // 1-100
  km: 100, // 1-100
  pa: 100, // 1-100
  kmp: 100, // 1-100
  sp: 100, // 1-100
  komentar: "Bagus",
};

const jsonWawancara = {
  pd: 5, // 1-5
  rrd: 5, // 1-5
  mdb: 5, // 1-5
  komentar: "Bagus",
};