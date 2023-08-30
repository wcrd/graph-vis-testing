<script>
    import TidyTree from "$lib/components/TidyTree.svelte";
    import SvelteTidyTree from "$lib/components/SvelteTidyTree.svelte";
</script>

<div class="container mx-auto">
    <h1 class="text-2xl my-2">Gallery of Graphs</h1>
    <hr/>
    <div class="my-2">
        <h1 class="text-xl">Tidy Tree</h1>
        <TidyTree />
    </div>
    <hr>
    <div class="my-2">
        <h1 class="text-xl">Svelte Tidy Tree</h1>
        <SvelteTidyTree />
    </div>

</div>

