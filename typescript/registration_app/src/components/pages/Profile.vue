<script setup lang="ts">
import type { UserProfileResponse } from "@/store";
import { ref, computed } from "vue";
import { useStore } from "vuex";

const store = useStore();
await store.dispatch("fetchProfile");

const PAGE_LENGTH = 10;

const profileData: UserProfileResponse = store.state.profile

const filter = ref("");
const page = ref(0);
const filteredTable = computed(() => 
    profileData.user_sessions.filter(row =>
        row.browser.includes(filter.value) || row.country.includes(filter.value) || row.ip.includes(filter.value) || row.time.includes(filter.value)
    )
)
const pagedTable = computed(() => {
    const startingIndex = page.value * PAGE_LENGTH;
    const endingIndex = Math.min((page.value + 1) * PAGE_LENGTH, filteredTable.value.length);
    return filteredTable.value.slice(startingIndex, endingIndex);
})

function modifyPage(update: number) {
    page.value += update;
    if (page.value < 0) {
        page.value = 0;
    }
    const nextPageThreshold = Math.floor(filteredTable.value.length / PAGE_LENGTH)
    if (
        page.value > nextPageThreshold || 
        (filteredTable.value.length % PAGE_LENGTH == 0 && page.value == nextPageThreshold)
    ) {
        page.value -= 1;
    }
}

function resetPage() {
    page.value = 0;
}

</script>
<template>
    <main>
        <section class="user-info">
            <img 
                src="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2F1.bp.blogspot.com%2F-mie_btrA0Lo%2FT-iVPR7EFnI%2FAAAAAAAAEjk%2Fgkd6ljpYlJ4%2Fs1600%2FBlue%2BSpace%2BWallpapers%2B1.jpg&f=1&nofb=1&ipt=3156c308ed86ec0557a08fe7cd77e6edb2388fb38e68ac5bcfb3a8803ac93219&ipo=images"
                alt="Avatar"
                width="100"
                height="100"
            /> 
            <p>
                {{ profileData.user_basics.first.toUpperCase() }} {{ profileData.user_basics.last.toUpperCase() }}
            </p>
        </section>
        <section>
            <input v-model="filter" @input="resetPage" type="text" placeholder="Filter table"/>
            <table>
                <thead>
                    <th>IP</th>
                    <th>Browser</th>
                    <th>Time</th>
                    <th>Country</th>
                </thead>
                <tbody>
                    <tr v-for="session in pagedTable">
                        <td>{{session.ip}}</td>
                        <td>{{session.browser}}</td>
                        <td>{{session.time}}</td>
                        <td>{{session.country}}</td>
                    </tr>
                </tbody>
            </table>
            <p>{{ filteredTable.length }} results</p>
            <p>{{ page }}</p>
            <button @click="modifyPage(-1)">Previous Page</button>
            <button @click="modifyPage(1)">Next Page</button>
        </section>
    </main>
</template>

<style scoped>
input {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
}

img {
  border-radius: 50%;
  margin-bottom: 1em;
}

table {
    border-collapse:collapse;
    border:1px solid #FF0000;
    table-layout: fixed;
    width: 75em;

}

th {
    text-align: left;
    font-weight: bold;
}

td, th {
    padding-left: 0.5em;
    border:1px solid #000000;
}



.user-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 5em;
}
</style>