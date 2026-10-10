local function debugPrint(message)
    if Config.Debug then
        print(('[police_station] %s'):format(message))
    end
end

CreateThread(function()
    debugPrint('Stage 1 scaffold loaded. Custom map assets are not installed yet.')

    while true do
        local sleep = 1000
        local playerCoords = GetEntityCoords(PlayerPedId())

        for key, point in pairs(Config.Points) do
            local distance = #(playerCoords - point.coords)

            if distance < 30.0 and Config.DrawMarkers then
                sleep = 0
                DrawMarker(
                    1,
                    point.coords.x, point.coords.y, point.coords.z - 1.0,
                    0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0,
                    0.45, 0.45, 0.25,
                    45, 115, 190, 140,
                    false, false, 2, false, nil, nil, false
                )
            end

            if distance <= Config.InteractDistance and IsControlJustReleased(0, 38) then
                BeginTextCommandThefeedPost('STRING')
                AddTextComponentSubstringPlayerName(point.label .. ' — interaction placeholder')
                EndTextCommandThefeedPostTicker(false, false)
                debugPrint(('Placeholder interaction used: %s'):format(key))
                Wait(700)
            end
        end

        Wait(sleep)
    end
end)
