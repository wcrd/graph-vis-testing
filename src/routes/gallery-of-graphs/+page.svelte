<script>
    import DirectedGraph from "$lib/components/DirectedGraph.svelte";
    import TidyTree from "$lib/components/TidyTree.svelte";
</script>

<div class="container mx-auto">
    <h1 class="text-2xl my-2">Gallery of Graphs</h1>
    <hr/>
    <div class="my-2">
        <h1 class="text-xl">Directed Graph</h1>
        <DirectedGraph />
    </div>
    <hr>
    <div class="my-2">
        <h1 class="text-xl">Tidy Tree</h1>
        <TidyTree />
    </div>
    

</div>

