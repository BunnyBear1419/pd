Config = {}

-- This is a scaffold. The custom building is not included in Stage 1.
Config.Debug = true
Config.DrawMarkers = true
Config.InteractDistance = 2.0

-- Replace every placeholder coordinate after selecting and placing the MLO.
-- Values are intentionally near the origin so they are obvious during setup.
Config.Points = {
    public_lobby = {
        label = 'Police HQ — Public Lobby',
        coords = vector3(0.0, 0.0, 0.0),
        heading = 0.0
    },
    booking = {
        label = 'Police HQ — Booking',
        coords = vector3(2.0, 0.0, 0.0),
        heading = 0.0
    },
    evidence = {
        label = 'Police HQ — Evidence',
        coords = vector3(4.0, 0.0, 0.0),
        heading = 0.0
    },
    armory = {
        label = 'Police HQ — Armory',
        coords = vector3(6.0, 0.0, 0.0),
        heading = 0.0
    },
    roof_access = {
        label = 'Police HQ — Roof Access',
        coords = vector3(8.0, 0.0, 0.0),
        heading = 0.0
    },
    garage = {
        label = 'Police HQ — Vehicle Garage',
        coords = vector3(10.0, 0.0, 0.0),
        heading = 0.0
    }
}
