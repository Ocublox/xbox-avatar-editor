import bpy

# Define the base name pattern to search for
base_pattern = ''  # Change this to match your objects

# Automatically find all TEXCOORD objects matching the pattern
sources = []
for obj in bpy.data.objects:
    if obj.name.startswith(base_pattern) and '_TEXCOORD' in obj.name:
        # Check if object has a UVMap
        if obj.type == 'MESH' and obj.data.uv_layers:
            # Find the first UV map (or you can specify which one)
            uv_map_name = obj.data.uv_layers[0].name
            sources.append((obj.name, uv_map_name))
            print(f"Found: {obj.name} with UV map '{uv_map_name}'")

if not sources:
    print(f"ERROR: No objects found matching pattern '{base_pattern}_TEXCOORD*'")
    raise SystemExit

# Sort sources to ensure consistent ordering (TEXCOORD, TEXCOORD1, TEXCOORD2, etc.)
sources.sort()

print(f"\nFound {len(sources)} source objects:")
for src in sources:
    print(f"  - {src[0]}")

# Generate target name from base pattern
target_name = f"{base_pattern}_merged"

print(f"\n=== Starting Multiple UV Map Copy ===")
print(f"Generated target name: {target_name}")

# Check if target exists, if not create it from first source
if target_name not in bpy.data.objects:
    print(f"Target '{target_name}' doesn't exist. Creating full copy from first source...")
    
    # Get first source
    first_source_name = sources[0][0]
    first_source = bpy.data.objects[first_source_name]
    
    # Duplicate the entire object (including all data)
    target = first_source.copy()
    target.data = first_source.data.copy()
    target.name = target_name
    target.data.name = target_name
    
    # Copy transform
    target.location = first_source.location.copy()
    target.rotation_euler = first_source.rotation_euler.copy()
    target.scale = first_source.scale.copy()
    
    # Link to same collection as first source
    for collection in first_source.users_collection:
        collection.objects.link(target)
    
    # Clear all UV maps from the new target (we'll rebuild them from all sources)
    while target.data.uv_layers:
        target.data.uv_layers.remove(target.data.uv_layers[0])
    
    print(f"✓ Created full copy '{target_name}' with {len(target.data.loops)} loops")
else:
    target = bpy.data.objects[target_name]
    print(f"Target '{target_name}' already exists")

print(f"Target: {target.name} has {len(target.data.loops)} loops")

# Process each source object
for source_name, uv_map_name in sources:
    print(f"\n--- Processing {source_name} ---")
    
    if source_name not in bpy.data.objects:
        print(f"ERROR: Source '{source_name}' not found! Skipping...")
        continue
    
    source = bpy.data.objects[source_name]
    print(f"Source: {source.name} has {len(source.data.loops)} loops")
    
    # Check if they have matching topology
    if len(source.data.loops) != len(target.data.loops):
        print(f"ERROR: {source_name} has different topology! Skipping...")
        continue
    
    # Get source UV layer
    if uv_map_name not in source.data.uv_layers:
        print(f"ERROR: UV map '{uv_map_name}' not found in {source_name}! Skipping...")
        continue
    
    source_uv = source.data.uv_layers[uv_map_name]
    print(f"Source UV layer '{uv_map_name}' has {len(source_uv.data)} coordinates")
    
    # Extract TEXCOORD suffix from source name (e.g., "head-right_TEXCOORD1" -> "TEXCOORD1")
    if '_TEXCOORD' in source_name:
        suffix = source_name.split('_TEXCOORD')[1]  # Gets "" or "1" or "2"
        target_uv_name = f"{uv_map_name}_TEXCOORD{suffix}"
    else:
        target_uv_name = uv_map_name  # Fallback to original name
    
    # Create or get target UV layer
    if target_uv_name in target.data.uv_layers:
        target_uv = target.data.uv_layers[target_uv_name]
        print(f"UV map '{target_uv_name}' already exists, overwriting...")
    else:
        target_uv = target.data.uv_layers.new(name=target_uv_name)
        print(f"Created new UV map '{target_uv_name}'")
    
    # Copy each UV coordinate
    for i in range(len(source_uv.data)):
        target_uv.data[i].uv = source_uv.data[i].uv.copy()
    
    print(f"✓ Copied {len(target_uv.data)} UV coordinates to '{target_uv_name}'!")

# Set target as active
bpy.context.view_layer.objects.active = target
target.select_set(True)

print(f"\n=== Verification ===")
print(f"{target.name} now has these UV maps:")
for uv_layer in target.data.uv_layers:
    print(f"  - {uv_layer.name}: {len(uv_layer.data)} UV coordinates")

print(f"\n✓✓✓ DONE! {target_name} now has all UV maps.")
