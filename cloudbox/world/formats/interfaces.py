# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Attribute, Interface

class IWorldFormat(Interface):
    """
    I am a World Format.
    """

    name = Attribute("The name of the world format.")
    supportsLoading = Attribute("Whether I support loading worlds from this format.")
    supportsSaving = Attribute("Whether I support saving worlds to this format.")

    def loadWorld(filepath):
        """
        Loads a world from filepath. Returns a dictionary with the following items:
            levelName: level name
            x: Length
            y: Width
            z: Height
            spawn: Spawn of world. A tuple of (x, y, z).
            blocksArray: Array of blocks. Expects an 1D array.
        The following items are optional:
            CreatedBy: { // The creator of this map.
                Service: Minecraft or ClassiCube.
                Username: Username.
            }
            MapGeneratorUsed: { // How this map was created.
                Software: Software used to create this map.
                MapGeneratorName: Map generator name. Can be string or None.
            }
            TimeCreated: Time of level creation. Unix timestamp.
            LastAccessed: Last time it was accessed.
            LastModified: Last time it was modified.
            Metadata, BlockMetadata, BlockMetadataAI, FreeBlockMetadataEntries: See docs/worldFormat.

        """

    def saveWorld(filepath):
        """
        Saves a world from filepath.
        """

