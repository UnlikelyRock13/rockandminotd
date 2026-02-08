#!/usr/bin/env python3
"""
Generate Rock & Mineral of the Day pages and RSS feed
Creates individual HTML pages for each day plus a homepage index
"""

from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

# Curated lists of rocks and minerals
rocks = [
    {"name": "Granite", "desc": "A coarse-grained intrusive igneous rock composed mainly of quartz, feldspar, and mica. Widely used as a construction and decorative stone."},
    {"name": "Basalt", "desc": "A dark, fine-grained volcanic rock that makes up most of the ocean floor. Forms from rapidly cooled lava."},
    {"name": "Sandstone", "desc": "A sedimentary rock composed mainly of sand-sized mineral particles or rock fragments."},
    {"name": "Limestone", "desc": "A sedimentary rock composed largely of calcite. Forms from marine organisms and chemical precipitation."},
    {"name": "Marble", "desc": "A metamorphic rock formed from limestone under heat and pressure. Prized for sculpture and architecture."},
    {"name": "Slate", "desc": "A fine-grained metamorphic rock that splits into thin sheets. Used for roofing and flooring."},
    {"name": "Schist", "desc": "A medium-grade metamorphic rock with visible mineral grains aligned in parallel layers."},
    {"name": "Gneiss", "desc": "A high-grade metamorphic rock with alternating light and dark bands. Very hard and durable."},
    {"name": "Obsidian", "desc": "Volcanic glass formed from rapidly cooled lava. Sharp edges made it valuable for tools and weapons."},
    {"name": "Pumice", "desc": "A vesicular volcanic rock so full of gas bubbles that it can float on water."},
    {"name": "Andesite", "desc": "An intermediate volcanic rock named after the Andes Mountains where it's common."},
    {"name": "Rhyolite", "desc": "A fine-grained volcanic rock with high silica content. The volcanic equivalent of granite."},
    {"name": "Shale", "desc": "A fine-grained sedimentary rock formed from clay and silt. The most common sedimentary rock."},
    {"name": "Conglomerate", "desc": "A sedimentary rock composed of rounded pebbles and cobbles cemented together."},
    {"name": "Breccia", "desc": "Similar to conglomerate but composed of angular rock fragments cemented together."},
    {"name": "Diorite", "desc": "An intrusive igneous rock intermediate in composition between granite and gabbro."},
    {"name": "Gabbro", "desc": "A coarse-grained intrusive igneous rock, the plutonic equivalent of basalt."},
    {"name": "Peridotite", "desc": "A dense, coarse-grained igneous rock composed mainly of olivine and pyroxene."},
    {"name": "Dunite", "desc": "An ultramafic rock composed almost entirely of olivine."},
    {"name": "Tuff", "desc": "A rock formed from consolidated volcanic ash."},
    {"name": "Mudstone", "desc": "A fine-grained sedimentary rock composed of clay and silt particles."},
    {"name": "Siltstone", "desc": "A sedimentary rock composed mainly of silt-sized particles."},
    {"name": "Quartzite", "desc": "A hard metamorphic rock formed from sandstone. Very resistant to weathering."},
    {"name": "Anthracite", "desc": "The highest grade of coal. Very hard and has the highest carbon content."},
    {"name": "Bituminous coal", "desc": "A relatively soft coal containing a tar-like substance called bitumen. The most abundant type of coal."},
    {"name": "Lignite", "desc": "A soft brownish coal showing traces of plant structure. The lowest grade of coal."},
    {"name": "Dolomite rock", "desc": "A sedimentary carbonate rock composed primarily of the mineral dolomite."},
    {"name": "Chert", "desc": "A hard, fine-grained sedimentary rock composed of microcrystalline quartz."},
    {"name": "Phyllite", "desc": "A metamorphic rock intermediate between slate and schist with a silky sheen."},
    {"name": "Migmatite", "desc": "A high-grade metamorphic rock showing both igneous and metamorphic characteristics."}
]

minerals = [
    {"name": "Quartz", "desc": "One of the most abundant minerals in Earth's crust. Composed of silicon and oxygen, it's very hard and comes in many varieties."},
    {"name": "Feldspar", "desc": "The most abundant mineral group in Earth's crust, comprising about 60% of terrestrial rocks."},
    {"name": "Calcite", "desc": "A carbonate mineral and the main component of limestone and marble. Reacts with dilute acid."},
    {"name": "Gypsum", "desc": "A soft sulfate mineral used to make plaster of Paris and drywall. Can form large transparent crystals."},
    {"name": "Halite", "desc": "Rock salt. Forms from evaporation of seawater. Essential for human life and historically valuable for trade."},
    {"name": "Pyrite", "desc": "Known as 'fool's gold' for its metallic luster and pale brass-yellow color. An iron sulfide mineral."},
    {"name": "Magnetite", "desc": "A black magnetic iron oxide. The most magnetic of all naturally occurring minerals on Earth."},
    {"name": "Hematite", "desc": "The main ore of iron. Named from the Greek word for blood due to its red color when powdered."},
    {"name": "Garnet", "desc": "A group of silicate minerals used as gemstones and abrasives. Commonly deep red but can be many colors."},
    {"name": "Olivine", "desc": "A green silicate mineral common in Earth's mantle. The gem variety is called peridot."},
    {"name": "Mica", "desc": "A group of silicate minerals known for their perfect sheet-like cleavage and flexibility."},
    {"name": "Talc", "desc": "The softest mineral (hardness 1 on Mohs scale). Used in cosmetics and as a lubricant."},
    {"name": "Fluorite", "desc": "A colorful halide mineral that fluoresces under UV light. Used in optics and metallurgy."},
    {"name": "Apatite", "desc": "A group of phosphate minerals. The main component of tooth enamel and bones."},
    {"name": "Orthoclase", "desc": "A common potassium feldspar mineral. An important component of granite."},
    {"name": "Plagioclase", "desc": "A series of sodium-calcium feldspar minerals. Very common in igneous rocks."},
    {"name": "Hornblende", "desc": "A dark amphibole mineral common in igneous and metamorphic rocks."},
    {"name": "Augite", "desc": "A black or dark green pyroxene mineral common in basalt and gabbro."},
    {"name": "Serpentine", "desc": "A group of green minerals formed by alteration of olivine and pyroxene. Often used as decorative stone."},
    {"name": "Kaolinite", "desc": "A white clay mineral used in ceramics and paper manufacturing."},
    {"name": "Chalcopyrite", "desc": "The most abundant copper ore mineral. Has a brass-yellow color."},
    {"name": "Galena", "desc": "The primary ore of lead. Forms cubic crystals with perfect cleavage."},
    {"name": "Sphalerite", "desc": "The primary ore of zinc. Can be various colors but often brown or black."},
    {"name": "Barite", "desc": "A heavy sulfate mineral used in drilling mud and as a source of barium."},
    {"name": "Graphite", "desc": "A soft form of carbon used in pencils and lubricants. The most stable form of carbon under standard conditions."},
    {"name": "Diamond", "desc": "The hardest natural substance. A form of carbon crystallized under extreme pressure and temperature."},
    {"name": "Corundum", "desc": "The second hardest mineral after diamond. Includes ruby and sapphire varieties."},
    {"name": "Beryl", "desc": "A beryllium silicate mineral. Gem varieties include emerald and aquamarine."},
    {"name": "Topaz", "desc": "A hard silicate mineral often used as a gemstone. Can be many colors."},
    {"name": "Tourmaline", "desc": "A complex boron silicate mineral that comes in many colors. Often used as a gemstone."},
    {"name": "Zircon", "desc": "A zirconium silicate mineral used in geochronology and as a gemstone."},
    {"name": "Amphibole", "desc": "A group of dark silicate minerals important in igneous and metamorphic rocks."},
    {"name": "Chlorite", "desc": "A green sheet silicate mineral common in low-grade metamorphic rocks."},
    {"name": "Epidote", "desc": "A green calcium aluminum silicate mineral common in metamorphic rocks."},
    {"name": "Dolomite", "desc": "A carbonate mineral similar to limestone but contains magnesium. Used as a source of magnesia."}
]

def get_day_of_year(date):
    """Calculate day of year (1-366) for a given date"""
    start = datetime(date.year, 1, 1)
    return (date - start).days + 1

def get_specimens_for_date(date):
    """Get rock and mineral for a specific date"""
    day = get_day_of_year(date)
    rock_index = day % len(rocks)
    mineral_index = day % len(minerals)
    return rocks[rock_index], minerals[mineral_index]

def create_daily_page(date, rock, mineral, base_url):
    """Create individual HTML page for a specific day"""
    date_str = date.strftime('%Y-%m-%d')
    formatted_date = date.strftime('%B %d, %Y')
    
    # Escape single quotes in descriptions for JavaScript
    rock_desc = rock['desc'].replace("'", "\\'")
    mineral_desc = mineral['desc'].replace("'", "\\'")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rock['name']} & {mineral['name']} - Rock & Mineral of the Day</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const {{ useState, useEffect }} = React;

        const DailyPage = () => {{
            const [rockData, setRockData] = useState(null);
            const [mineralData, setMineralData] = useState(null);
            const [loading, setLoading] = useState(true);

            const rockName = "{rock['name']}";
            const mineralName = "{mineral['name']}";
            const rockDesc = `{rock_desc}`;
            const mineralDesc = `{mineral_desc}`;

            useEffect(() => {{
                const fetchData = async (name, isRock) => {{
                    const fallback = {{
                        title: name,
                        extract: isRock ? rockDesc : mineralDesc,
                        thumbnail: null,
                        url: `https://en.wikipedia.org/wiki/${{encodeURIComponent(name)}}`
                    }};

                    try {{
                        const params = new URLSearchParams({{
                            action: 'query',
                            format: 'json',
                            prop: 'extracts|pageimages',
                            exintro: true,
                            explaintext: true,
                            piprop: 'thumbnail|original',
                            pithumbsize: 800,
                            titles: name,
                            origin: '*',
                            redirects: 1
                        }});

                        const response = await fetch(`https://en.wikipedia.org/w/api.php?${{params}}`);
                        if (!response.ok) return fallback;

                        const data = await response.json();
                        const pages = data.query.pages;
                        const pageId = Object.keys(pages)[0];
                        const pageData = pages[pageId];

                        if (pageId === '-1' || !pageData.extract) return fallback;

                        return {{
                            title: pageData.title,
                            extract: pageData.extract,
                            thumbnail: pageData.thumbnail,
                            url: `https://en.wikipedia.org/wiki/${{encodeURIComponent(name)}}`
                        }};
                    }} catch (err) {{
                        return fallback;
                    }}
                }};

                const loadData = async () => {{
                    const [rock, mineral] = await Promise.all([
                        fetchData(rockName, true),
                        fetchData(mineralName, false)
                    ]);
                    setRockData(rock);
                    setMineralData(mineral);
                    setLoading(false);
                }};

                loadData();
            }}, []);

            if (loading) {{
                return (
                    <div className="min-h-screen bg-gradient-to-br from-slate-800 to-slate-900 flex items-center justify-center">
                        <p className="text-slate-300 text-lg">Loading...</p>
                    </div>
                );
            }}

            return (
                <div className="min-h-screen bg-gradient-to-br from-slate-800 to-slate-900 p-4 md:p-8">
                    <div className="max-w-4xl mx-auto">
                        <div className="text-center mb-8">
                            <h1 className="text-4xl md:text-5xl font-bold text-cyan-400 mb-2">
                                🪨 Rock & Mineral of the Day
                            </h1>
                            <p className="text-slate-300 text-lg">{formatted_date}</p>
                            <a href="{base_url}" className="text-cyan-400 hover:text-cyan-300 text-sm mt-2 inline-block">← Back to All Posts</a>
                        </div>

                        <div className="mb-8">
                            <h2 className="text-2xl font-bold text-cyan-300 mb-4 flex items-center gap-2">
                                <span className="text-3xl">🪨</span> Today's Rock
                            </h2>
                            <div className="bg-slate-700/50 backdrop-blur rounded-xl shadow-2xl overflow-hidden border border-slate-600">
                                {{rockData.thumbnail && (
                                    <div className="relative h-64 md:h-96 bg-slate-900">
                                        <img 
                                            src={{rockData.thumbnail.source}} 
                                            alt={{rockData.title}}
                                            className="w-full h-full object-contain p-4"
                                        />
                                    </div>
                                )}}
                                <div className="p-6 md:p-8">
                                    <h3 className="text-3xl md:text-4xl font-bold text-cyan-300 mb-4">
                                        {{rockData.title}}
                                    </h3>
                                    <p className="text-slate-200 text-lg leading-relaxed mb-6">
                                        {{rockData.extract}}
                                    </p>
                                    <a 
                                        href={{rockData.url}}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="bg-cyan-500 hover:bg-cyan-600 text-slate-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200 inline-block"
                                    >
                                        Learn More on Wikipedia
                                    </a>
                                </div>
                            </div>
                        </div>

                        <div className="mb-8">
                            <h2 className="text-2xl font-bold text-emerald-300 mb-4 flex items-center gap-2">
                                <span className="text-3xl">💎</span> Today's Mineral
                            </h2>
                            <div className="bg-slate-700/50 backdrop-blur rounded-xl shadow-2xl overflow-hidden border border-slate-600">
                                {{mineralData.thumbnail && (
                                    <div className="relative h-64 md:h-96 bg-slate-900">
                                        <img 
                                            src={{mineralData.thumbnail.source}} 
                                            alt={{mineralData.title}}
                                            className="w-full h-full object-contain p-4"
                                        />
                                    </div>
                                )}}
                                <div className="p-6 md:p-8">
                                    <h3 className="text-3xl md:text-4xl font-bold text-emerald-300 mb-4">
                                        {{mineralData.title}}
                                    </h3>
                                    <p className="text-slate-200 text-lg leading-relaxed mb-6">
                                        {{mineralData.extract}}
                                    </p>
                                    <a 
                                        href={{mineralData.url}}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="bg-emerald-500 hover:bg-emerald-600 text-slate-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200 inline-block"
                                    >
                                        Learn More on Wikipedia
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }};

        ReactDOM.render(<DailyPage />, document.getElementById('root'));
    </script>
</body>
</html>"""
    
    return html

def create_index_page(dates_and_specimens, base_url):
    """Create homepage with list of all posts"""
    
    posts_html = ""
    for date, rock, mineral in dates_and_specimens:
        date_str = date.strftime('%Y-%m-%d')
        formatted_date = date.strftime('%B %d, %Y')
        
        # Escape quotes for JSX
        rock_desc_short = rock['desc'][:100].replace('"', '\\"').replace("'", "\\'") + "..."
        mineral_desc_short = mineral['desc'][:100].replace('"', '\\"').replace("'", "\\'") + "..."
        
        posts_html += f'''
                    <a href="{base_url}/{date_str}.html" className="block bg-slate-700/50 backdrop-blur rounded-lg p-6 border border-slate-600 hover:border-cyan-400 transition-colors duration-200">
                        <div className="flex items-start gap-4">
                            <div className="text-4xl">🪨💎</div>
                            <div className="flex-1">
                                <h2 className="text-2xl font-bold text-cyan-300 mb-2">
                                    {rock['name']} & {mineral['name']}
                                </h2>
                                <p className="text-slate-400 text-sm mb-3">{formatted_date}</p>
                                <div className="space-y-2">
                                    <p className="text-slate-300"><span className="text-cyan-400 font-semibold">Rock:</span> {rock_desc_short}</p>
                                    <p className="text-slate-300"><span className="text-emerald-400 font-semibold">Mineral:</span> {mineral_desc_short}</p>
                                </div>
                            </div>
                        </div>
                    </a>'''
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rock & Mineral of the Day</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const IndexPage = () => {{
            return (
                <div className="min-h-screen bg-gradient-to-br from-slate-800 to-slate-900 p-4 md:p-8">
                    <div className="max-w-4xl mx-auto">
                        <div className="text-center mb-12">
                            <h1 className="text-5xl md:text-6xl font-bold text-cyan-400 mb-4">
                                🪨 Rock & Mineral of the Day
                            </h1>
                            <p className="text-slate-300 text-lg">
                                Daily geology education featuring rocks and minerals from Wikipedia
                            </p>
                        </div>

                        <div className="space-y-6">
                            {posts_html}
                        </div>

                        <div className="mt-12 bg-slate-700/30 rounded-lg p-6 text-center">
                            <p className="text-slate-300">
                                Subscribe to the <a href="{base_url}/feed.xml" className="text-cyan-400 hover:text-cyan-300 underline">RSS feed</a> to get daily updates
                            </p>
                        </div>
                    </div>
                </div>
            );
        }};

        ReactDOM.render(<IndexPage />, document.getElementById('root'));
    </script>
</body>
</html>"""
    
    return html

def create_rss_feed(dates_and_specimens, base_url):
    """Generate RSS feed with recent posts"""
    now = datetime.utcnow()
    
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = 'Rock & Mineral of the Day'
    ET.SubElement(channel, 'link').text = base_url
    ET.SubElement(channel, 'description').text = 'Daily geology education featuring a different rock and mineral each day from Wikipedia'
    ET.SubElement(channel, 'language').text = 'en-us'
    ET.SubElement(channel, 'lastBuildDate').text = now.strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    atom_link = ET.SubElement(channel, 'atom:link')
    atom_link.set('href', f'{base_url}/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Add items for each date (most recent first)
    for date, rock, mineral in dates_and_specimens:
        date_str = date.strftime('%Y-%m-%d')
        formatted_date = date.strftime('%B %d, %Y')
        
        item = ET.SubElement(channel, 'item')
        
        title = f"{rock['name']} & {mineral['name']} - {formatted_date}"
        ET.SubElement(item, 'title').text = title
        
        # Link to the specific daily page
        ET.SubElement(item, 'link').text = f"{base_url}/{date_str}.html"
        
        description = f"""<h2>🪨 Today's Rock: {rock['name']}</h2>
<p>{rock['desc']}</p>
<p><a href="https://en.wikipedia.org/wiki/{rock['name'].replace(' ', '_')}">Learn more about {rock['name']} on Wikipedia</a></p>

<h2>💎 Today's Mineral: {mineral['name']}</h2>
<p>{mineral['desc']}</p>
<p><a href="https://en.wikipedia.org/wiki/{mineral['name'].replace(' ', '_')}">Learn more about {mineral['name']} on Wikipedia</a></p>

<p><em>Visit the <a href="{base_url}/{date_str}.html">full post</a> for images and complete Wikipedia articles.</em></p>"""
        
        ET.SubElement(item, 'description').text = description
        
        guid = ET.SubElement(item, 'guid', isPermaLink='true')
        guid.text = f"{base_url}/{date_str}.html"
        
        pub_date = date.replace(hour=6, minute=0, second=0, microsecond=0)
        ET.SubElement(item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    xml_str = minidom.parseString(ET.tostring(rss)).toprettyxml(indent='  ')
    return xml_str

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = 'https://yourusername.github.io/rockandminotd'
    
    # Generate pages for last 30 days
    now = datetime.utcnow()
    dates_and_specimens = []
    
    for days_ago in range(30):
        date = now - timedelta(days=days_ago)
        rock, mineral = get_specimens_for_date(date)
        dates_and_specimens.append((date, rock, mineral))
        
        # Create daily page
        date_str = date.strftime('%Y-%m-%d')
        page_html = create_daily_page(date, rock, mineral, base_url)
        
        with open(f'{date_str}.html', 'w', encoding='utf-8') as f:
            f.write(page_html)
        
        print(f"Created {date_str}.html - {rock['name']} & {mineral['name']}")
    
    # Create index page
    index_html = create_index_page(dates_and_specimens, base_url)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("Created index.html")
    
    # Create RSS feed
    feed_xml = create_rss_feed(dates_and_specimens, base_url)
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(feed_xml)
    print("Created feed.xml")
    
    print(f"\nGenerated 30 daily pages, index, and RSS feed successfully!")
