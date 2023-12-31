<script>
    import * as d3 from 'd3'
    import { onMount } from 'svelte';

    import DataDirectedGraph from '../../working/data_directedGraph.json'

    let el;

	// const data = [
	// 	{ source: 'target', target: 'pnt_1', type: 'hasPoint' },
	// 	{ source: 'target', target: 'pnt_2', type: 'hasPoint' },
	// 	{ source: 'target', target: 'vav_1', type: 'feeds' },
	// 	{ source: 'vav_1', target: 'vav_1_dmpr', type: 'hasPart' },
	// 	{ source: 'vav_1_dmpr', target: 'pnt_3', type: 'hasPoint' },
	// ];

    const data = DataDirectedGraph;
    
	const width = 900;
	const height = 600;
	const types = Array.from(new Set(data.map((d) => d.type)));
	// const nodes = Array.from(new Set(data.flatMap((l) => [l.source, l.target])), (id) => ({ id }));
    const nodes = Object.values(
        data
            .flatMap(l => [{"id":l.target, "className":l.target_class}, {"id": l.source, className: l.source_class}])
            .reduce((acc, val) => ({ ...acc, [val.id]: val}), {})
    )
	const links = data.map((d) => Object.create(d));

    // console.debug(nodes, data)

	const color = d3.scaleOrdinal(types, d3.schemeCategory10);

    const drag = simulation => {
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
        
        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    function linkArc(d) {
        const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
        return `
            M${d.source.x},${d.source.y}
            A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
        `;
    }
    
    onMount(()=> {
        const simulation = d3
            .forceSimulation(nodes)
            .force(
                'link',
                d3.forceLink(links).id((d) => d.id)
            )
            .force('charge', d3.forceManyBody().strength(-400))
            .force('x', d3.forceX())
            .force('y', d3.forceY());

        const svg = d3.select(el).append("svg")
            .attr("viewBox", [-width / 2, -height / 2, width, height])
            .attr("width", width)
            .attr("height", height)
            .attr("style", "max-width: 100%; height: auto; font: 12px sans-serif;");

        // Per-type markers, as they don't inherit styles.
        svg.append("defs").selectAll("marker")
        .data(types)
        .join("marker")
            .attr("id", d => `arrow-${d}`)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -0.5)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
        .append("path")
            .attr("fill", color)
            .attr("d", "M0,-5L10,0L0,5");

        const link = svg.append("g")
            .attr("fill", "none")
            .attr("stroke-width", 1.5)
        .selectAll("path")
        .data(links)
        .join("path")
            .attr("stroke", d => color(d.type))
            .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

        const node = svg.append("g")
            .attr("fill", "currentColor")
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
        .selectAll("g")
        .data(nodes)
        .join("g")
            .call(drag(simulation));
        

        node.append("circle")
            .attr("stroke", "white")
            .attr("stroke-width", 1.5)
            .attr("fill", d => d.id=="target" ? 'red' : 'black')
            .attr("r", d => d.id=="target" ? 8 : 4 );

        node.append("text")
            .attr("x", 8)
            .attr("y", "0.31em")
            .text(d => `${d.id} (${d.className})`)
        .clone(true).lower()
            .attr("fill", "none")
            .attr("stroke", "white")
            .attr("stroke-width", 3);

        simulation.on("tick", () => {
            link.attr("d", linkArc);
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });

        invalidation.then(() => simulation.stop());

        Object.assign(svg.node(), {scales: {color}});
    })
</script>

<!-- <svg {width} {height}>
    {#each types as t, i}
        <marker key={`arrow-${i}`}>X</marker>
    {/each}

    {#each nodes as n, i}
        <circle key={`node-${i}`} r={4}></circle>
    {/each}
</svg> -->

<div class="border rounded-md my-1 py-5 flex flex-col items-center">
    
    <div bind:this={el}></div>

    <div id="legend" class="flex flex-row gap-x-5 mt-5">
        <div class="flex flex-row gap-x-2 items-center">
            <span class="block h-3 w-3 rounded-full bg-yellow-500"></span>
            Has Part
        </div>
        <div class="flex flex-row gap-x-2 items-center">
            <span class="block h-3 w-3 rounded-full bg-blue-500"></span>
            Feeds
        </div>
        <div class="flex flex-row gap-x-2 items-center">
            <span class="block h-3 w-3 rounded-full bg-green-500"></span>
            Has Point
        </div>
    </div>
</div>