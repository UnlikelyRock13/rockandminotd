#!/usr/bin/env python3
"""
Generate RSS feed for Rock & Mineral of the Day
Single item per day - optimized for Readwise Reader
"""

from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

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

def create_rss_feed(base_url):
    """Generate RSS feed XML with only today's item"""
    now = datetime.utcnow()  # Use UTC time
    rock, mineral = get_specimens_for_date(now)
    
    # Create RSS structure
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    
    channel = ET.SubElement(rss, 'channel')
    
    # Channel metadata
    ET.SubElement(channel, 'title').text = 'Rock & Mineral of the Day'
    ET.SubElement(channel, 'link').text = base_url
    ET.SubElement(channel, 'description').text = 'Daily geology education featuring a different rock and mineral each day from Wikipedia'
    ET.SubElement(channel, 'language').text = 'en-us'
    ET.SubElement(channel, 'lastBuildDate').text = now.strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    # Self-reference
    atom_link = ET.SubElement(channel, 'atom:link')
    atom_link.set('href', f'{base_url}/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Create item for today ONLY
    item = ET.SubElement(channel, 'item')
    
    # Title: "Rock Name & Mineral Name - Date"
    title = f"{rock['name']} & {mineral['name']} - {now.strftime('%B %d, %Y')}"
    ET.SubElement(item, 'title').text = title
    
    # Link to the page
    ET.SubElement(item, 'link').text = base_url
    
    # Description: Combined rock and mineral info
    description = f"""<h2>🪨 Today's Rock: {rock['name']}</h2>
<p>{rock['desc']}</p>
<p><a href="https://en.wikipedia.org/wiki/{rock['name'].replace(' ', '_')}">Learn more about {rock['name']} on Wikipedia</a></p>

<h2>💎 Today's Mineral: {mineral['name']}</h2>
<p>{mineral['desc']}</p>
<p><a href="https://en.wikipedia.org/wiki/{mineral['name'].replace(' ', '_')}">Learn more about {mineral['name']} on Wikipedia</a></p>

<p><em>Visit the <a href="{base_url}">Rock & Mineral of the Day</a> page for images and full Wikipedia articles.</em></p>"""
    
    ET.SubElement(item, 'description').text = description
    
    # GUID: unique identifier for this day (critical for RSS readers)
    guid = ET.SubElement(item, 'guid', isPermaLink='false')
    guid.text = f"rockmineral-{now.strftime('%Y%m%d')}"
    
    # Publication date - use current time to ensure it's "new"
    ET.SubElement(item, 'pubDate').text = now.strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    # Pretty print XML
    xml_str = minidom.parseString(ET.tostring(rss)).toprettyxml(indent='  ')
    
    return xml_str

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = 'https://yourusername.github.io/rock-of-the-day'
    
    feed_xml = create_rss_feed(base_url)
    
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(feed_xml)
    
    today_rock, today_mineral = get_specimens_for_date(datetime.utcnow())
    print(f"RSS feed generated successfully!")
    print(f"Today's specimens: {today_rock['name']} & {today_mineral['name']}")
