#!/usr/bin/env python3
"""Generate the Pokemon FireRed AI knowledge base from a pinned pret checkout.

Only Python's standard library is required. The generated Markdown is a view of
the canonical JSON records, so factual tables are never maintained twice.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path


SOURCE_COMMIT = "df4449a27cd78dd747ce269e47d3ab4a0149d8f4"
ROM_SHA1 = "41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc"
VERSION = "Pokemon FireRed (USA) GBA v1.0"
AVAILABILITY = {"normal", "optional", "trade_required", "event_required", "version_specific", "unavailable_normally"}


CHAPTERS = [
    {
        "number": 1, "slug": "introducao-pallet-town", "title": "Introdução e Pallet Town",
        "areas": ["PalletTown", "PalletTown_PlayersHouse", "PalletTown_RivalsHouse", "PalletTown_ProfessorOaksLab"],
        "start": "Novo jogo iniciado no quarto do protagonista, sem Pokémon.",
        "prerequisites": ["Nenhum."],
        "prep": ["Retire a Potion do PC antes de sair.", "Escolha o starter sabendo que ele define as equipes futuras do rival e o Legendary Beast do pós-game."],
        "actions": [
            "Saia de casa e tente entrar na Route 1 para acionar Professor Oak.",
            "No laboratório, escolha Bulbasaur, Charmander ou Squirtle e confirme o nome do rival.",
            "Vença ou conclua a primeira batalha contra o rival; use a Potion se necessário.",
            "Saia do laboratório em direção à Route 1."
        ],
        "end": "Starter recebido; primeira batalha do rival resolvida; Route 1 liberada.",
        "revisits": ["Voltar após receber Oak's Parcel para obter Pokédex e Poké Balls."],
        "strategy": "Bulbasaur oferece o começo mais seguro; Squirtle é equilibrado; Charmander exige mais preparação para Pewter Gym."
    },
    {
        "number": 2, "slug": "route-1-viridian-retorno", "title": "Route 1, Viridian City e retorno a Pallet Town",
        "areas": ["Route1", "ViridianCity", "ViridianCity_Mart", "PalletTown_ProfessorOaksLab", "Route2"],
        "start": "Starter obtido; nenhuma Pokédex; acesso ao norte por Route 1.",
        "prerequisites": ["Concluir a primeira batalha do rival."],
        "prep": ["Fale com o funcionário da Poké Mart na Route 1 para uma Potion.", "Use o Pokémon Center de Viridian se estiver ferido."],
        "actions": [
            "Atravesse Route 1 e entre na Viridian City Poké Mart para receber Oak's Parcel.",
            "Retorne ao laboratório de Oak e entregue o pacote.",
            "Receba Pokédex e Poké Balls; visite Daisy na casa do rival para obter Town Map.",
            "Capture opções iniciais em Route 1 e Route 22, se desejado.",
            "Compre Antidotes e Potions antes de entrar em Route 2 e Viridian Forest."
        ],
        "end": "Pokédex, Poké Balls e acesso à Viridian Forest disponíveis.",
        "revisits": ["Route 2 leste exige Cut; o portão de Victory Road só será útil após as Badges."],
        "strategy": "Mankey na Route 22 ajuda equipes com Charmander contra Brock."
    },
    {
        "number": 3, "slug": "viridian-forest-pewter", "title": "Viridian Forest, Pewter City e Boulder Badge",
        "areas": ["ViridianForest", "PewterCity", "PewterCity_Mart", "PewterCity_Gym", "PewterCity_Museum"],
        "start": "Pokédex recebida; entrada sul de Viridian Forest.",
        "prerequisites": ["Entregar Oak's Parcel."],
        "prep": ["Leve Antidotes para Poison Sting.", "Treine a equipe aproximadamente até níveis 10–12."],
        "actions": [
            "Percorra Viridian Forest recolhendo todos os item balls e enfrentando os Bug Catchers.",
            "Em Pewter City, cure a equipe e visite o museu se quiser registrar o conteúdo opcional.",
            "Desafie Pewter Gym e derrote Brock.",
            "Receba Boulder Badge e TM39 Rock Tomb.",
            "Saia pelo leste; receba Running Shoes do ajudante de Oak."
        ],
        "end": "Boulder Badge obtida; Route 3 liberada.",
        "revisits": ["Voltar ao museu com Cut para obter Old Amber."],
        "strategy": "Golpes Grass, Water ou Fighting resolvem o Gym; evite depender apenas de golpes Normal contra a defesa de Onix."
    },
    {
        "number": 4, "slug": "route-3-mt-moon-route-4", "title": "Route 3, Mt. Moon e Route 4",
        "areas": ["Route3", "Route4", "Route4_PokemonCenter", "MtMoon"],
        "start": "Boulder Badge obtida; saída leste de Pewter City.",
        "prerequisites": ["Derrotar Brock."],
        "prep": ["Compre Poké Balls, Potions e Antidotes.", "Deixe espaço na equipe se pretender comprar Magikarp."],
        "actions": [
            "Enfrente todos os treinadores da Route 3 e registre os encounters locais.",
            "No Pokémon Center, compre Magikarp apenas se aceitar o investimento de treino.",
            "Atravesse os três níveis de Mt. Moon, recolha itens e enfrente Team Rocket.",
            "Derrote o Super Nerd e escolha Helix Fossil ou Dome Fossil; o outro fica indisponível neste save.",
            "Na Route 4, use os Move Tutors de Mega Punch/Mega Kick se fizer sentido e siga para Cerulean."
        ],
        "end": "Cerulean City alcançada; um fóssil escolhido.",
        "revisits": ["Mt. Moon possui itens que exigem exploração completa; não é possível voltar pelo ressalto da Route 4 imediatamente."],
        "strategy": "Conserve recursos para o rival e Nugget Bridge; Paras pode fornecer suporte, mas possui muitas fraquezas."
    },
    {
        "number": 5, "slug": "cerulean-routes-24-25", "title": "Cerulean, Cascade Badge, Routes 24–25 e Bill",
        "areas": ["CeruleanCity", "CeruleanCity_Mart", "CeruleanCity_Gym", "Route24", "Route25", "Route5", "UndergroundPath_NorthEntrance", "UndergroundPath_B1F"],
        "start": "Primeira chegada a Cerulean City.",
        "prerequisites": ["Sair de Mt. Moon pela Route 4."],
        "prep": ["Mire em níveis 16–20.", "Leve resposta para Water e para a equipe variável do rival."],
        "actions": [
            "Derrote Misty para obter Cascade Badge e TM03 Water Pulse; a ordem com o norte é flexível.",
            "Vença o rival ao norte e atravesse Nugget Bridge, recusando ou aceitando a proposta da Rocket sem alterar o resultado.",
            "Explore Route 24 e Route 25, enfrente todos os treinadores e ajude Bill em Sea Cottage.",
            "Receba S.S. Ticket e retorne a Cerulean.",
            "Passe pela casa invadida, derrote o Rocket Grunt e obtenha TM28 Dig.",
            "Siga por Route 5 e Underground Path até Route 6."
        ],
        "end": "Cascade Badge e S.S. Ticket obtidos; caminho para Vermilion aberto.",
        "revisits": ["A Day Care da Route 5 aceita um Pokémon por vez.", "Cerulean Cave permanece bloqueada até o pós-game."],
        "strategy": "Oddish é exclusivo de FireRed nessa fase e ajuda contra Misty; Pikachu também é uma resposta direta."
    },
    {
        "number": 6, "slug": "route-6-vermilion-ss-anne", "title": "Route 6, Vermilion City, S.S. Anne e Thunder Badge",
        "areas": ["Route6", "VermilionCity", "VermilionCity_Mart", "VermilionCity_Gym", "SSAnne"],
        "start": "Saída sul do Underground Path na Route 6.",
        "prerequisites": ["Obter S.S. Ticket."],
        "prep": ["Leve a equipe curada para explorar todo o navio antes de enfrentar o rival.", "Capture Diglett se precisar de resposta Ground para Lt. Surge."],
        "actions": [
            "Explore Route 6 e Vermilion; obtenha Old Rod e Bike Voucher.",
            "Embarque na S.S. Anne e explore todos os cômodos, itens e treinadores antes de avançar.",
            "Derrote o rival e fale com o capitão para receber HM01 Cut.",
            "Ensine Cut a um Pokémon adequado; ao sair, a S.S. Anne parte definitivamente.",
            "Resolva os interruptores do Vermilion Gym, derrote Lt. Surge e receba Thunder Badge e TM34 Shock Wave."
        ],
        "end": "Cut utilizável fora de batalha; Thunder Badge obtida.",
        "revisits": ["Troque Bike Voucher pela Bicycle em Cerulean.", "A S.S. Anne não pode ser revisitada após a partida."],
        "strategy": "Diglett/Dugtrio neutraliza a maior parte do Gym, mas cuidado com o nível e a baixa resistência."
    },
    {
        "number": 7, "slug": "route-11-diglett-route-9", "title": "Route 11, Diglett's Cave, Route 2 leste e Route 9",
        "areas": ["Route11", "Route11_EastEntrance", "DiglettsCave", "Route2", "PewterCity_Museum", "Route9", "Route10"],
        "start": "Cut disponível após a S.S. Anne.",
        "prerequisites": ["Obter HM01 e Thunder Badge para usá-lo fora de batalha."],
        "prep": ["Capture pelo menos 10 espécies para o aide de Flash.", "Leve Cut na equipe."],
        "actions": [
            "Explore Route 11, enfrente os treinadores e visite o gate para Itemfinder quando tiver 30 espécies.",
            "Atravesse Diglett's Cave até Route 2 leste.",
            "Receba HM05 Flash do aide de Oak se tiver 10 espécies capturadas.",
            "Use Cut para revisitar o Pewter Museum e obter Old Amber.",
            "Retorne a Cerulean, pegue Bicycle e siga por Route 9 até o Pokémon Center da Route 10."
        ],
        "end": "Entrada de Rock Tunnel alcançada; Flash disponível se o requisito da Pokédex foi cumprido.",
        "revisits": ["Itemfinder exige 30 espécies; Exp. Share na Route 15 exige 50."],
        "strategy": "Flash não é obrigatório tecnicamente, mas reduz erros e encontros desperdiçados no Rock Tunnel."
    },
    {
        "number": 8, "slug": "rock-tunnel-lavender-celadon", "title": "Rock Tunnel, Lavender Town e chegada a Celadon",
        "areas": ["RockTunnel", "Route10", "LavenderTown", "LavenderTown_Mart", "Route8", "UndergroundPath_WestEntrance", "UndergroundPath_EastEntrance", "Route7"],
        "start": "Pokémon Center da Route 10, diante de Rock Tunnel.",
        "prerequisites": ["Alcançar Route 10; Flash recomendado."],
        "prep": ["Leve Escape Rope, Potions e cura de status.", "Reserve PP para vários Hikers e Pokémaniacs."],
        "actions": [
            "Atravesse Rock Tunnel coletando os itens e usando o tutor de Rock Slide se desejado.",
            "Desça Route 10 até Lavender Town e visite Pokémon Tower apenas para registrar o bloqueio do fantasma.",
            "Siga pela Route 8 e use Underground Path, pois o gate de Saffron está bloqueado.",
            "Atravesse Route 7 e entre em Celadon City."
        ],
        "end": "Celadon City acessível; Rocket Hideout e Rainbow Badge disponíveis.",
        "revisits": ["Pokémon Tower só pode ser concluída após obter Silph Scope."],
        "strategy": "Rock/Ground e Selfdestruct são os maiores riscos do túnel; mantenha HP acima de faixas críticas."
    },
    {
        "number": 9, "slug": "celadon-rocket-pokemon-tower", "title": "Celadon City, Rocket Hideout e Pokémon Tower",
        "areas": ["CeladonCity", "CeladonCity_DepartmentStore", "CeladonCity_GameCorner", "CeladonCity_GameCorner_PrizeRoom", "CeladonCity_Gym", "RocketHideout", "PokemonTower", "LavenderTown"],
        "start": "Primeira chegada a Celadon City.",
        "prerequisites": ["Atravessar Route 7."],
        "prep": ["Obtenha Eevee, Coin Case e Tea antes de sair da cidade.", "Compre recursos no Department Store."],
        "actions": [
            "Explore Celadon, Department Store, Game Corner, Mansion e restaurantes; registre gifts e lojas especiais.",
            "Derrote Erika no Celadon Gym para Rainbow Badge e TM19 Giga Drain.",
            "Revele a escada no Game Corner, atravesse Rocket Hideout e derrote Giovanni para Silph Scope.",
            "Retorne a Lavender e suba Pokémon Tower, vencendo o rival, Channelers e o espírito Marowak.",
            "Derrote os Rockets no topo, resgate Mr. Fuji e receba Poké Flute."
        ],
        "end": "Silph Scope e Poké Flute obtidos; Snorlax pode ser removido das Routes 12 e 16.",
        "revisits": ["Use Tea para abrir os gates de Saffron.", "Game Corner exige Coin Case e coins para prêmios."],
        "strategy": "Não gaste todas as moedas sem conferir os prêmios exclusivos de FireRed e as TMs de alto valor."
    },
    {
        "number": 10, "slug": "routes-12-18-fuchsia", "title": "Routes 12–18, Safari Zone, Fuchsia e Soul Badge",
        "areas": ["Route12", "Route13", "Route14", "Route15", "Route16", "Route17", "Route18", "FuchsiaCity", "FuchsiaCity_Mart", "FuchsiaCity_Gym", "SafariZone"],
        "start": "Poké Flute obtida; caminhos para Fuchsia disponíveis.",
        "prerequisites": ["Resgatar Mr. Fuji."],
        "prep": ["Leve Poké Balls para os Snorlax; salve antes de acordá-los.", "Tenha Bicycle para Cycling Road."],
        "actions": [
            "Escolha Route 12–15 ou Cycling Road como primeiro caminho, mas explore ambos para cobertura total.",
            "Acorde e capture ou derrote os dois Snorlax; recolha Super Rod e demais itens das rotas.",
            "No Safari Zone, alcance Secret House dentro do limite, obtenha HM03 Surf e recolha Gold Teeth.",
            "Entregue Gold Teeth ao Warden para HM04 Strength.",
            "Derrote Koga no Fuchsia Gym para Soul Badge e TM06 Toxic.",
            "Complete o segundo caminho entre Celadon e Fuchsia e registre todos os treinadores."
        ],
        "end": "Surf e Strength disponíveis; Soul Badge obtida.",
        "revisits": ["Exp. Share no gate da Route 15 exige 50 espécies capturadas.", "Safari Zone possui encontros por subárea e itens perdíveis por tentativa, não permanentemente."],
        "strategy": "Use várias entradas no Safari Zone se necessário; priorize HM03 e Gold Teeth antes de caçar raridades."
    },
    {
        "number": 11, "slug": "saffron-silph-gym", "title": "Saffron City, Silph Co., Fighting Dojo e Marsh Badge",
        "areas": ["SaffronCity", "SaffronCity_Mart", "SaffronCity_Dojo", "SaffronCity_Gym", "SilphCo"],
        "start": "Tea obtido em Celadon; Saffron acessível por qualquer gate.",
        "prerequisites": ["Entregar Tea ao guarda."],
        "prep": ["Leve cura suficiente para Silph Co.", "Tenha resposta para Psychic e para a equipe do rival."],
        "actions": [
            "Explore Fighting Dojo e escolha Hitmonlee ou Hitmonchan após vencer o mestre.",
            "Atravesse Silph Co., obtenha Card Key e abra todas as salas para itens e treinadores.",
            "Receba Lapras no 7F, vença o rival e derrote Giovanni no 11F.",
            "Receba Master Ball do presidente.",
            "Resolva os teleports de Saffron Gym, derrote Sabrina e obtenha Marsh Badge e TM04 Calm Mind."
        ],
        "end": "Team Rocket expulsa de Saffron; Master Ball e Marsh Badge obtidas.",
        "revisits": ["O segundo prêmio do Fighting Dojo fica indisponível neste save sem trade."],
        "strategy": "Silph Co. possui cura gratuita no 9F; use-a para evitar retornar ao Pokémon Center."
    },
    {
        "number": 12, "slug": "routes-19-20-seafoam", "title": "Routes 19–20 e Seafoam Islands",
        "areas": ["Route19", "Route20", "SeafoamIslands"],
        "start": "Surf e Strength utilizáveis fora de batalha.",
        "prerequisites": ["Soul Badge; Strength disponível."],
        "prep": ["Leve Ultra Balls e cura para status Ice/Water.", "Salve antes de Articuno."],
        "actions": [
            "Surfe ao sul de Fuchsia pela Route 19, enfrentando todos os Swimmers.",
            "Entre em Seafoam Islands e empurre os boulders corretos para bloquear as correntes.",
            "Explore todos os andares e capture Articuno se desejar.",
            "Saia pelo lado oeste e conclua Route 20 até Cinnabar Island."
        ],
        "end": "Cinnabar Island alcançada; Seafoam atravessada e Articuno resolvido.",
        "revisits": ["Também é possível chegar a Cinnabar pela Route 21 a partir de Pallet após Surf."],
        "strategy": "Não empurre boulders sem observar o nível inferior; movimentos errados exigem reiniciar a sala."
    },
    {
        "number": 13, "slug": "cinnabar-mansion-gym", "title": "Cinnabar Island, Pokémon Mansion e Volcano Badge",
        "areas": ["CinnabarIsland", "CinnabarIsland_Mart", "CinnabarIsland_PokemonLab", "PokemonMansion", "CinnabarIsland_Gym"],
        "start": "Primeira chegada a Cinnabar Island.",
        "prerequisites": ["Surf; alcançar Cinnabar por Route 20 ou 21."],
        "prep": ["Leve Pokémon com Water, Ground ou Rock.", "Deposite um Pokémon se for reviver fósseis."],
        "actions": [
            "Visite o laboratório, faça os in-game trades desejados e entregue Fossil/Old Amber para reviver Pokémon.",
            "Explore Pokémon Mansion, use as estátuas para alternar portas e recolha todos os itens visíveis e ocultos.",
            "Obtenha Secret Key no B1F.",
            "Abra Cinnabar Gym, responda aos quizzes ou enfrente os treinadores e derrote Blaine.",
            "Receba Volcano Badge e TM38 Fire Blast; aceite a viagem de Bill às Sevii Islands."
        ],
        "end": "Volcano Badge obtida; primeira visita às Sevii Islands iniciada ou disponível.",
        "revisits": ["O laboratório leva tempo em passos para reviver fósseis; saia e retorne.", "Itens ocultos da Mansion exigem inspeção por andar."],
        "strategy": "Repels economizam recursos na Mansion, mas desative-os ao registrar os encounters por piso."
    },
    {
        "number": 14, "slug": "sevii-parte-1", "title": "Sevii Islands I: One, Two e Three Island",
        "areas": ["OneIsland", "TwoIsland", "ThreeIsland", "KindleRoad", "MtEmber", "CapeBrink", "BondBridge", "BerryForest"],
        "start": "Viagem com Bill após derrotar Blaine.",
        "prerequisites": ["Volcano Badge."],
        "prep": ["Mantenha Surf e Strength.", "Leve Poké Balls para Moltres em Mt. Ember."],
        "actions": [
            "Em One Island, fale com Celio e receba Tri-Pass e Meteorite.",
            "Explore Kindle Road, Ember Spa e Mt. Ember; capture Moltres e use o Move Tutor de Explosion se desejado.",
            "Em Two Island, visite Game Corner e descubra o desaparecimento de Lostelle.",
            "Em Three Island, derrote os Bikers, atravesse Bond Bridge e encontre Lostelle em Berry Forest.",
            "Derrote o Hypno, devolva Lostelle e entregue Meteorite; retorne com Bill."
        ],
        "end": "Lostelle resgatada; acesso normal ao continente restaurado; Viridian Gym disponível.",
        "revisits": ["Cape Brink possui Move Tutor ligado ao tipo do starter.", "Conteúdo completo de Four–Seven Island exige National Pokédex."],
        "strategy": "Faça Mt. Ember nesta visita para evitar retrabalho, mas a captura de Moltres pode ser adiada."
    },
    {
        "number": 15, "slug": "route-21-power-plant-viridian", "title": "Route 21, Power Plant e Earth Badge",
        "areas": ["Route21", "PowerPlant", "Route10", "ViridianCity_Gym", "ViridianCity"],
        "start": "Retorno das Sevii Islands; sete Badges.",
        "prerequisites": ["Concluir a missão de Lostelle."],
        "prep": ["Leve Ultra Balls para Zapdos.", "Prepare respostas Water/Grass/Ice para Ground no Viridian Gym."],
        "actions": [
            "Explore Route 21 entre Cinnabar e Pallet, incluindo treinadores e encontros aquáticos.",
            "Use Surf na Route 10 para entrar na Power Plant; diferencie Electrode disfarçados de item balls.",
            "Recolha itens e capture Zapdos se desejado.",
            "Volte a Viridian, resolva o Gym e derrote Giovanni.",
            "Receba Earth Badge e TM26 Earthquake."
        ],
        "end": "Oito Badges obtidas; entrada para Pokémon League liberada.",
        "revisits": ["Legendary captures podem ser adiadas, mas registre o estado de cada encontro único."],
        "strategy": "Não use Master Ball automaticamente em Zapdos; guarde-a para o roamer se preferir eliminar a fuga."
    },
    {
        "number": 16, "slug": "routes-22-23-victory-road", "title": "Routes 22–23 e Victory Road",
        "areas": ["Route22", "Route23", "VictoryRoad"],
        "start": "Oito Badges obtidas em Viridian City.",
        "prerequisites": ["Earth Badge."],
        "prep": ["Equipe por volta dos níveis 45–50.", "Leve Surf e Strength, além de cura e Escape Rope."],
        "actions": [
            "Vença a última batalha pré-Liga contra o rival na Route 22.",
            "Atravesse os oito checkpoints da Route 23 apresentando cada Badge.",
            "Em Victory Road, use boulders nos switches, enfrente todos os treinadores e recolha itens.",
            "Use o Move Tutor de Double-Edge apenas após decidir o usuário.",
            "Saia no Indigo Plateau."
        ],
        "end": "Indigo Plateau alcançado; Elite Four disponível.",
        "revisits": ["Alguns itens exigem manipular novamente os boulders e trocar de andar."],
        "strategy": "Preserve PP; Pokémon selvagens e treinadores de Victory Road são uma boa preparação final."
    },
    {
        "number": 17, "slug": "indigo-plateau-liga", "title": "Indigo Plateau e Pokémon League",
        "areas": ["IndigoPlateau", "PokemonLeague"],
        "start": "Indigo Plateau; primeira tentativa da Liga.",
        "prerequisites": ["Atravessar Victory Road."],
        "prep": ["Compre Full Restores, Revives e cura de status.", "Salve antes de entrar; não é possível sair entre membros."],
        "actions": [
            "Derrote Lorelei, Bruno, Agatha e Lance em sequência.",
            "Cure e reorganize itens entre as salas.",
            "Derrote o rival Champion, cuja equipe depende do starter escolhido.",
            "Registre a equipe no Hall of Fame e continue o save."
        ],
        "end": "Primeiro Hall of Fame concluído; pós-game habilitado.",
        "revisits": ["A Liga recebe equipes mais fortes após concluir a missão Ruby/Sapphire."],
        "strategy": "Cobertura Electric, Ice, Psychic e Water reduz a necessidade de uma equipe excessivamente treinada."
    },
    {
        "number": 18, "slug": "pos-game-four-six-island", "title": "Pós-game I: National Pokédex, Four Island e Six Island",
        "areas": ["PalletTown_ProfessorOaksLab", "OneIsland", "MtEmber", "FourIsland", "IcefallCave", "SixIsland", "RuinValley", "DottedHole"],
        "start": "Primeiro Hall of Fame concluído.",
        "prerequisites": ["Registrar ao menos 60 espécies para receber National Pokédex."],
        "prep": ["Leve Cut, Surf e Strength.", "Converse com Celio para iniciar a busca das gems."],
        "actions": [
            "Receba National Pokédex e Rainbow Pass.",
            "Retorne a Mt. Ember, derrote os Rockets e obtenha Ruby.",
            "Entregue Ruby a Celio e viaje a Four Island; explore Icefall Cave e ajude Lorelei contra Team Rocket.",
            "Em Six Island, atravesse Water Path e Ruin Valley.",
            "Abra Dotted Hole usando Cut na porta, resolva os buracos e presencie o roubo de Sapphire."
        ],
        "end": "Ruby entregue; Sapphire localizada e roubada; senha parcial do Rocket Warehouse obtida.",
        "revisits": ["Four Island contém Day Care de breeding.", "Altering Cave possui apenas Zubat sem distribuição externa no GBA comum."],
        "strategy": "Capture espécies novas das Sevii Islands para ampliar a National Pokédex durante o trajeto."
    },
    {
        "number": 19, "slug": "pos-game-five-seven-island", "title": "Pós-game II: Five Island, Rocket Warehouse e Seven Island",
        "areas": ["FiveIsland", "FiveIsland_Meadow", "FiveIsland_RocketWarehouse", "ResortGorgeous", "LostCave", "MemorialPillar", "WaterLabyrinth", "SevenIsland", "TrainerTower", "SevaultCanyon", "TanobyRuins", "TanobyChambers"],
        "start": "Sapphire roubada em Dotted Hole.",
        "prerequisites": ["Obter as duas senhas do Rocket Warehouse."],
        "prep": ["Leve equipe para longas áreas sem atalhos.", "Mantenha Cut, Surf e Strength."],
        "actions": [
            "Explore Five Isle Meadow e entre no Rocket Warehouse com as duas senhas.",
            "Derrote os Admins, recupere Sapphire e entregue-a a Celio para liberar conexão com Hoenn.",
            "Complete Resort Gorgeous, Lost Cave, Memorial Pillar e Water Labyrinth.",
            "Em Seven Island, explore Trainer Tower e Sevault Canyon.",
            "Resolva Tanoby Key e visite todas as Tanoby Chambers para os diferentes Unown."
        ],
        "end": "Sapphire entregue; rede de Celio concluída; conteúdo principal das Sevii Islands resolvido.",
        "revisits": ["Trainer Tower possui modos e equipes próprios.", "Lost Cave usa sequência direcional; erros retornam à entrada."],
        "strategy": "Separe a coleta de Unown por chamber para não confundir pools de encontros."
    },
    {
        "number": 20, "slug": "cerulean-cave-liga-round-2", "title": "Cerulean Cave, Mewtwo, Legendary Beast e League Round 2",
        "areas": ["CeruleanCave", "IndigoPlateau", "PokemonLeague"],
        "start": "Ruby e Sapphire entregues; National Pokédex ativa.",
        "prerequisites": ["Concluir a rede de Celio e o primeiro Hall of Fame."],
        "prep": ["Leve Ultra/Timer Balls e um controlador de status para Mewtwo.", "Monte equipe próxima dos níveis 60–65 para a revanche."],
        "actions": [
            "Entre em Cerulean Cave, explore todos os andares e recolha itens visíveis e ocultos.",
            "Salve antes de Mewtwo e capture ou resolva o encontro de nível 70.",
            "Localize o Legendary Beast definido pelo starter: Entei, Suicune ou Raikou, nível 50 e roaming.",
            "Retorne ao Indigo Plateau e derrote as equipes atualizadas da Elite Four e Champion."
        ],
        "end": "Mewtwo e roamer resolvidos conforme o estado registrado; League Round 2 concluída.",
        "revisits": ["O roamer preserva HP e status ao fugir; pode desaparecer por bug se usar Roar na versão original."],
        "strategy": "Master Ball é especialmente valiosa no roamer; Mewtwo pode ser controlado com status e Timer Balls."
    },
    {
        "number": 21, "slug": "eventos-birth-navel", "title": "Conteúdo de evento: Birth Island e Navel Rock",
        "areas": ["BirthIsland", "NavelRock"],
        "start": "Save no pós-game; eventos não liberados em uma partida GBA comum.",
        "prerequisites": ["AuroraTicket para Birth Island.", "MysticTicket para Navel Rock.", "Distribuição oficial ou alteração externa legítima do save/cartucho."],
        "prep": ["Salve antes de cada encontro único.", "Leve equipe de captura e muitas Balls."],
        "actions": [
            "Com AuroraTicket, viaje a Birth Island e resolva o puzzle do triângulo sem passos extras para enfrentar Deoxys nível 30.",
            "Com MysticTicket, viaje a Navel Rock.",
            "Desça até Lugia nível 70 e suba até Ho-Oh nível 70, registrando ambos separadamente.",
            "Marque o conteúdo como event_required; não o apresente como normalmente acessível no FireRed GBA v1.0."
        ],
        "end": "Deoxys, Lugia e Ho-Oh resolvidos quando os tickets existem; caso contrário, conteúdo documentado como indisponível normalmente.",
        "revisits": ["Os tickets eram distribuições limitadas e não fazem parte do fluxo normal da ROM GBA v1.0."],
        "strategy": "Não confunda a disponibilidade do relançamento Switch com a autoridade GBA deste guia."
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def stable_id(prefix: str, *parts: object) -> str:
    raw = "|".join(str(p) for p in parts)
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")[:90]
    digest = hashlib.sha1(raw.encode()).hexdigest()[:8]
    return f"{prefix}-{slug}-{digest}"


def strip_const(value: str, prefix: str) -> str:
    return value.removeprefix(prefix).replace("_", " ").title().replace("Pokemon", "Pokémon").replace("Tm", "TM").replace("Hm", "HM")


def human_map(name: str) -> str:
    was_constant = name.startswith("MAP_")
    name = name.removeprefix("MAP_")
    name = name.replace("_", " ")
    if was_constant:
        name = name.title()
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", name)
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)
    replacements = {
        "SS Anne": "S.S. Anne", "SSAnne": "S.S. Anne", "Mt Moon": "Mt. Moon", "Mt Ember": "Mt. Ember",
        "Digletts": "Diglett's", "Players": "Player's", "Rivals": "Rival's",
        "Oaks": "Oak's", "Loreleis": "Lorelei's", "Brunos": "Bruno's", "Agathas": "Agatha's",
        "Lances": "Lance's", "Champions": "Champion's", "Copycats": "Copycat's", "Wardens": "Warden's",
        "Pokemon": "Pokémon", "Pokemonmansion": "Pokémon Mansion",
        "Pokemon Mansion": "Pokémon Mansion", "Silph Co": "Silph Co.", "Route 1 0": "Route 10",
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    name = re.sub(r"Route(\d+)", r"Route \1", name)
    return name.strip()


def brace_blocks(text: str, header_re: str):
    for match in re.finditer(header_re, text, re.M):
        start = text.find("{", match.end() - 1)
        if start < 0:
            continue
        depth = 0
        for pos in range(start, len(text)):
            if text[pos] == "{": depth += 1
            elif text[pos] == "}":
                depth -= 1
                if depth == 0:
                    yield match, text[start + 1:pos]
                    break


def source_ref(relative: str, line: int | None = None) -> dict:
    return {"repository": "pret/pokefirered", "commit": SOURCE_COMMIT, "path": relative, "line": line}


def load_maps(src: Path):
    areas, map_by_const, objects_by_script = [], {}, defaultdict(list)
    for path in sorted((src / "data/maps").glob("*/map.json")):
        data = json.loads(read(path))
        map_id = data["id"]
        area = {
            "id": stable_id("area", map_id), "map_id": map_id, "name_en": human_map(data.get("name", map_id)),
            "aliases": [data.get("name", ""), data.get("region_map_section", "")],
            "map_type": data.get("map_type"), "requires_flash": bool(data.get("requires_flash")),
            "connections": data.get("connections", []), "warp_count": len(data.get("warp_events", [])),
            "availability": "normal", "source": source_ref(str(path.relative_to(src)).replace("\\", "/"))
        }
        areas.append(area); map_by_const[map_id] = area
        for obj in data.get("object_events", []):
            if obj.get("script"):
                objects_by_script[obj["script"]].append({"map_id": map_id, "x": obj.get("x"), "y": obj.get("y"), "graphics_id": obj.get("graphics_id"), "trainer_type": obj.get("trainer_type")})
    return areas, map_by_const, objects_by_script


def load_encounters(src: Path, map_by_const: dict):
    doc = json.loads(read(src / "src/data/wild_encounters.json"))
    group = doc["wild_encounter_groups"][0]
    field_rates = {f["type"]: f["encounter_rates"] for f in group["fields"]}
    fishing_groups = next(f["groups"] for f in group["fields"] if f["type"] == "fishing_mons")
    records = []
    for enc in group["encounters"]:
        label = enc.get("base_label", "")
        if "LeafGreen" in label or ("_FireRed" not in label and "FireRed" not in label):
            continue
        map_id = enc["map"]
        altering_match = re.search(r"AlteringCave_(\d+)_FireRed", label)
        encounter_variant = f"event_pool_{altering_match.group(1)}" if altering_match else "default"
        availability = "unavailable_normally" if altering_match else "normal"
        area_name = map_by_const.get(map_id, {}).get("name_en", human_map(map_id))
        for field in ("land_mons", "water_mons", "rock_smash_mons"):
            if field not in enc: continue
            method = {"land_mons": "land", "water_mons": "surf", "rock_smash_mons": "rock_smash"}[field]
            rates = field_rates[field]
            for slot, mon in enumerate(enc[field].get("mons", [])):
                rate = rates[slot]
                records.append({
                    "id": stable_id("enc", label, method, slot, mon["species"], mon["min_level"], mon["max_level"]),
                    "area_id": map_by_const.get(map_id, {}).get("id"), "map_id": map_id, "area_name_en": area_name,
                    "method": method, "species": strip_const(mon["species"], "SPECIES_"),
                    "species_id": mon["species"], "min_level": mon["min_level"], "max_level": mon["max_level"],
                    "slot": slot, "slot_rate_percent": rate, "species_total_rate_percent": 0,
                    "encounter_table_id": label, "encounter_variant": encounter_variant,
                    "encounter_rate": enc[field].get("encounter_rate"), "availability": availability, "version": "FireRed",
                    "source": source_ref("src/data/wild_encounters.json")
                })
        if "fishing_mons" in enc:
            mons = enc["fishing_mons"].get("mons", [])
            rates = field_rates["fishing_mons"]
            for method, slots in fishing_groups.items():
                for local_slot, slot in enumerate(slots):
                    mon = mons[slot]; rate = rates[slot]
                    records.append({
                        "id": stable_id("enc", label, method, slot, mon["species"], mon["min_level"], mon["max_level"]),
                        "area_id": map_by_const.get(map_id, {}).get("id"), "map_id": map_id, "area_name_en": area_name,
                        "method": method, "species": strip_const(mon["species"], "SPECIES_"),
                        "species_id": mon["species"], "min_level": mon["min_level"], "max_level": mon["max_level"],
                        "slot": local_slot, "slot_rate_percent": rate, "species_total_rate_percent": 0,
                        "encounter_table_id": label, "encounter_variant": encounter_variant,
                        "encounter_rate": enc["fishing_mons"].get("encounter_rate"), "availability": availability, "version": "FireRed",
                        "source": source_ref("src/data/wild_encounters.json")
                    })
    totals = defaultdict(int)
    for r in records: totals[(r["encounter_table_id"], r["method"], r["species_id"])] += r["slot_rate_percent"]
    for r in records: r["species_total_rate_percent"] = totals[(r["encounter_table_id"], r["method"], r["species_id"])]
    return records


def collect_script_blocks(src: Path):
    blocks = {}
    patterns = list((src / "data").rglob("*.inc")) + list((src / "data").rglob("*.s"))
    for path in patterns:
        text = read(path)
        matches = list(re.finditer(r"(?m)^([A-Za-z0-9_]+)::\s*$", text))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            blocks[m.group(1)] = {"text": text[m.end():end], "path": path}
    return blocks


def load_items(src: Path, map_by_const: dict, objects_by_script: dict, blocks: dict, encounters: list):
    item_meta = {i["itemId"]: i for i in json.loads(read(src / "src/data/items.json"))["items"]}
    records, seen = [], set()

    def add(item_id, source_type, map_id, x, y, script, availability="optional", quantity=1, renewable=False, requirement=None):
        if not item_id.startswith("ITEM_") or item_id in {"ITEM_NONE"}: return
        key = (item_id, source_type, map_id, x, y, script)
        if key in seen: return
        seen.add(key)
        meta = item_meta.get(item_id, {})
        records.append({
            "id": stable_id("item", *key), "item_id": item_id,
            "item_name_en": meta.get("english", strip_const(item_id, "ITEM_")), "source_type": source_type,
            "area_id": map_by_const.get(map_id, {}).get("id") if map_id else None, "map_id": map_id,
            "area_name_en": map_by_const.get(map_id, {}).get("name_en", human_map(map_id)) if map_id else None,
            "coordinates": {"x": x, "y": y} if x is not None and y is not None else None,
            "directions_ptbr": f"Interaja com o objeto/NPC em {human_map(map_id)}, coordenadas ({x}, {y})." if map_id and x is not None else f"Obtenha em {human_map(map_id)} conforme o evento indicado." if map_id else "Consulte o evento de origem.",
            "quantity": quantity, "renewable": renewable, "requirement": requirement,
            "availability": availability, "price": meta.get("price"), "script": script,
            "source": source_ref(str(blocks.get(script, {}).get("path", src).relative_to(src)).replace("\\", "/") if script in blocks else "data/maps")
        })

    for path in sorted((src / "data/maps").glob("*/map.json")):
        data = json.loads(read(path)); map_id = data["id"]
        for bg in data.get("bg_events", []):
            if bg.get("type") == "hidden_item":
                add(bg["item"], "hidden", map_id, bg.get("x"), bg.get("y"), bg.get("flag", "hidden_item"), quantity=bg.get("quantity", 1), renewable="RENEWABLE" in bg.get("flag", ""))
        for obj in data.get("object_events", []):
            if "ITEM" not in obj.get("graphics_id", "") and "BALL" not in obj.get("graphics_id", ""): continue
            block = blocks.get(obj.get("script", ""), {}).get("text", "")
            m = re.search(r"\b(?:itemball|finditem)\s+(ITEM_[A-Z0-9_]+)(?:,\s*(\d+))?", block)
            if m: add(m.group(1), "visible", map_id, obj.get("x"), obj.get("y"), obj.get("script"), quantity=int(m.group(2) or 1))

    for label, info in blocks.items():
        map_id = None
        rel = str(info["path"].relative_to(src)).replace("\\", "/")
        mpath = re.match(r"data/maps/([^/]+)/", rel)
        if mpath:
            p = src / "data/maps" / mpath.group(1) / "map.json"
            if p.exists(): map_id = json.loads(read(p))["id"]
        coords = objects_by_script.get(label, [{}])[0]
        map_id = coords.get("map_id", map_id)
        gift_matches = list(re.finditer(r"\bgiveitem\s+(ITEM_[A-Z0-9_]+)(?:,\s*(\d+))?", info["text"]))
        gift_matches += list(re.finditer(r"\bgiveitem_msg\s+[^,\n]+,\s*(ITEM_[A-Z0-9_]+)(?:,\s*(\d+))?", info["text"]))
        for m in gift_matches:
            add(m.group(1), "gift", map_id, coords.get("x"), coords.get("y"), label, quantity=int(m.group(2) or 1), requirement="Condição definida pelo evento do NPC/script.")

    # Wild held items are a property of the encountered species. The engine uses
    # 50% for itemCommon and 5% for itemRare (or 100% when both are equal).
    held_by_species = {}
    species_text = read(src / "src/data/pokemon/species_info.h")
    for match, body in brace_blocks(species_text, r"\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*\{"):
        common = re.search(r"\.itemCommon\s*=\s*(ITEM_[A-Z0-9_]+)", body)
        rare = re.search(r"\.itemRare\s*=\s*(ITEM_[A-Z0-9_]+)", body)
        held_by_species[match.group(1)] = (common.group(1) if common else "ITEM_NONE", rare.group(1) if rare else "ITEM_NONE")
    encountered_pairs = sorted({(r["map_id"], r["species_id"], r["availability"]) for r in encounters})
    for map_id, species_id, availability in encountered_pairs:
        common, rare = held_by_species.get(species_id, ("ITEM_NONE", "ITEM_NONE"))
        for item_id, rarity, chance in ((common, "common", 100 if common == rare and common != "ITEM_NONE" else 50), (rare, "rare", 100 if common == rare and rare != "ITEM_NONE" else 5)):
            if item_id == "ITEM_NONE" or (rarity == "rare" and rare == common): continue
            meta = item_meta.get(item_id, {})
            key = (item_id, "held", map_id, species_id, rarity)
            if key in seen: continue
            seen.add(key)
            records.append({
                "id": stable_id("item", *key), "item_id": item_id,
                "item_name_en": meta.get("english", strip_const(item_id, "ITEM_")), "source_type": "held",
                "area_id": map_by_const.get(map_id, {}).get("id"), "map_id": map_id,
                "area_name_en": map_by_const.get(map_id, {}).get("name_en", human_map(map_id)), "coordinates": None,
                "directions_ptbr": f"Encontre {strip_const(species_id, 'SPECIES_')} selvagem nesta área e capture-o ou use Thief/Covet.",
                "quantity": 1, "renewable": True, "requirement": f"Held item {rarity}; chance base {chance}% por encontro da espécie.",
                "held_by_species_id": species_id, "held_item_rarity": rarity, "held_item_chance_percent": chance,
                "availability": availability, "price": meta.get("price"), "script": None,
                "source": source_ref("src/data/pokemon/species_info.h"), "chance_source": source_ref("src/pokemon.c", 6032)
            })

    return records, item_meta


def parse_parties(src: Path):
    text = read(src / "src/data/trainer_parties.h")
    parties = {}
    for match, body in brace_blocks(text, r"static const struct\s+\w+\s+(sParty_[A-Za-z0-9_]+)\[\]\s*=\s*\{"):
        mons = []
        for _, mon in brace_blocks("X={" + body + "};", r"X\s*=\s*\{"):
            # The wrapper returns the entire array; extract direct mon blocks instead.
            depth = 0; start = None
            for pos, ch in enumerate(mon):
                if ch == "{":
                    if depth == 0: start = pos
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0 and start is not None:
                        chunk = mon[start + 1:pos]
                        species = re.search(r"\.species\s*=\s*(SPECIES_[A-Z0-9_]+)", chunk)
                        level = re.search(r"\.lvl\s*=\s*(\d+)", chunk)
                        if species and level:
                            moves_m = re.search(r"\.moves\s*=\s*\{([^}]*)\}", chunk, re.S)
                            moves = re.findall(r"MOVE_[A-Z0-9_]+", moves_m.group(1)) if moves_m else []
                            held = re.search(r"\.heldItem\s*=\s*(ITEM_[A-Z0-9_]+)", chunk)
                            iv = re.search(r"\.iv\s*=\s*(\d+)", chunk)
                            mons.append({"species_id": species.group(1), "species": strip_const(species.group(1), "SPECIES_"), "level": int(level.group(1)), "iv": int(iv.group(1)) if iv else None, "held_item": held.group(1) if held else None, "moves": [strip_const(x, "MOVE_") for x in moves]})
                        start = None
            break
        parties[match.group(1)] = mons
    return parties


def load_trainers(src: Path, map_by_const: dict, objects_by_script: dict, blocks: dict):
    parties = parse_parties(src)
    class_names = {}
    for m in re.finditer(r"\[(TRAINER_CLASS_[A-Z0-9_]+)\]\s*=\s*_\(\"([^\"]*)\"\)", read(src / "src/data/text/trainer_class_names.h")):
        class_names[m.group(1)] = m.group(2).title()
    script_to_trainers = defaultdict(set)
    for label, info in blocks.items():
        for tid in re.findall(r"\btrainerbattle_[a-z0-9_]+\s+(TRAINER_[A-Z0-9_]+)", info["text"]): script_to_trainers[label].add(tid)
    locations = defaultdict(list)
    for script, tids in script_to_trainers.items():
        infos = objects_by_script.get(script, [])
        if infos:
            for tid in tids: locations[tid].extend(infos)
        else:
            rel = str(blocks[script]["path"].relative_to(src)).replace("\\", "/")
            m = re.match(r"data/maps/([^/]+)/", rel)
            if m:
                p = src / "data/maps" / m.group(1) / "map.json"
                if p.exists():
                    map_id = json.loads(read(p))["id"]
                    for tid in tids: locations[tid].append({"map_id": map_id, "x": None, "y": None, "script": script})

    rematch_map = defaultdict(list)
    vs = read(src / "src/vs_seeker.c")
    for m in re.finditer(r"\{\s*\{([^}]*)\}\s*,\s*MAP\((MAP_[A-Z0-9_]+)\)\s*\}", vs):
        ids = re.findall(r"TRAINER_[A-Z0-9_]+", m.group(1))
        for stage, tid in enumerate(ids): rematch_map[tid].append({"map_id": m.group(2), "stage": stage})

    trainer_text = read(src / "src/data/trainers.h")
    records = []
    for match, body in brace_blocks(trainer_text, r"\[(TRAINER_[A-Z0-9_]+)\]\s*=\s*\{"):
        tid = match.group(1)
        name = re.search(r"\.trainerName\s*=\s*_\(\"([^\"]*)\"\)", body)
        party = re.search(r"\.party\s*=\s*[A-Z0-9_]+\((sParty_[A-Za-z0-9_]+)\)", body)
        cls = re.search(r"\.trainerClass\s*=\s*(TRAINER_CLASS_[A-Z0-9_]+)", body)
        if not name or not name.group(1) or not party or not parties.get(party.group(1)): continue
        if tid not in locations and tid not in rematch_map and not any(k in tid for k in ("LEADER_", "ELITE_FOUR_", "CHAMPION_", "RIVAL_", "GIOVANNI")):
            continue
        locs = locations.get(tid) or [{"map_id": x["map_id"], "x": None, "y": None} for x in rematch_map.get(tid, [])]
        map_id = locs[0].get("map_id") if locs else None
        rematch_stage = next((x["stage"] for x in rematch_map.get(tid, [])), 0)
        if (tid.startswith("TRAINER_ELITE_FOUR_") and tid.endswith("_2")) or "TRAINER_CHAMPION_REMATCH_" in tid:
            rematch_stage = "league_round_2"
        mandatory = any(k in tid for k in ("LEADER_", "ELITE_FOUR_", "CHAMPION_", "GIOVANNI", "RIVAL_"))
        records.append({
            "id": stable_id("battle", tid), "trainer_id": tid, "trainer_name_en": name.group(1).title(),
            "trainer_class_id": cls.group(1) if cls else None, "trainer_class_en": class_names.get(cls.group(1), strip_const(cls.group(1), "TRAINER_CLASS_")) if cls else None,
            "map_id": map_id, "area_id": map_by_const.get(map_id, {}).get("id"), "area_name_en": map_by_const.get(map_id, {}).get("name_en", human_map(map_id)) if map_id else None,
            "coordinates": {"x": locs[0].get("x"), "y": locs[0].get("y")} if locs and locs[0].get("x") is not None else None,
            "mandatory": mandatory, "battle_type": "double" if re.search(r"\.doubleBattle\s*=\s*TRUE", body) else "single",
            "rematch_stage": rematch_stage, "party": parties[party.group(1)],
            "trainer_items": re.findall(r"ITEM_[A-Z0-9_]+", re.search(r"\.items\s*=\s*\{([^}]*)\}", body, re.S).group(1)) if re.search(r"\.items\s*=\s*\{([^}]*)\}", body, re.S) else [],
            "reward": "Prize money calculado pelo jogo a partir da classe e do maior nível; Amulet Coin pode dobrar o valor.",
            "availability": "optional" if not mandatory else "normal", "source": source_ref("src/data/trainers.h"), "party_source": source_ref("src/data/trainer_parties.h")
        })
    return sorted(records, key=lambda r: (r.get("map_id") or "ZZZ", r["trainer_id"]))


def load_trainer_tower(src: Path, map_by_const: dict):
    text = read(src / "src/trainer_tower_sets.c")
    floor_defs = {}
    for match, body in brace_blocks(text, r"static const struct TrainerTowerFloor\s+(sTrainerTowerFloor_[A-Za-z0-9_]+)\s*=\s*\{"):
        challenge = re.search(r"\.challengeType\s*=\s*(CHALLENGE_TYPE_[A-Z]+)", body)
        trainer_marks = list(re.finditer(r"\.name\s*=\s*_\(\"([^\"]*)\"\)", body))
        trainers = []
        for i, tm in enumerate(trainer_marks):
            name = tm.group(1)
            if not name: continue
            end = trainer_marks[i + 1].start() if i + 1 < len(trainer_marks) else len(body)
            segment = body[tm.end():end]
            facility = re.search(r"\.facilityClass\s*=\s*(FACILITY_CLASS_[A-Z0-9_]+)", segment)
            mon_marks = list(re.finditer(r"\.species\s*=\s*(SPECIES_[A-Z0-9_]+)", segment))
            mons = []
            for j, mm in enumerate(mon_marks):
                mend = mon_marks[j + 1].start() if j + 1 < len(mon_marks) else len(segment)
                chunk = segment[mm.start():mend]
                held = re.search(r"\.heldItem\s*=\s*(ITEM_[A-Z0-9_]+)", chunk)
                moves_m = re.search(r"\.moves\s*=\s*\{([^}]*)\}", chunk, re.S)
                moves = re.findall(r"MOVE_[A-Z0-9_]+", moves_m.group(1)) if moves_m else []
                mons.append({"species_id": mm.group(1), "species": strip_const(mm.group(1), "SPECIES_"), "level": "scaled_to_highest_party", "iv": None, "held_item": held.group(1) if held else None, "moves": [strip_const(x, "MOVE_") for x in moves]})
            if mons: trainers.append({"name": name.title(), "facility_class": facility.group(1) if facility else None, "mons": mons[:6]})
        if challenge and trainers: floor_defs[match.group(1)] = {"challenge": challenge.group(1), "trainers": trainers}

    pointer_area = text[text.find("const struct TrainerTowerFloor *const gTrainerTowerFloors"):]
    modes = {}
    for m in re.finditer(r"\[(CHALLENGE_TYPE_[A-Z]+)\]\s*=\s*\{([^}]*)\}", pointer_area, re.S):
        modes[m.group(1)] = re.findall(r"&?(sTrainerTowerFloor_[A-Za-z0-9_]+)", m.group(2))
    single_idx = [(0, 2), (1, 3), (2, 4), (3, 5), (4, 1), (5, 2), (0, 3), (1, 4)]
    double_idx = [(0, 1), (1, 3), (2, 0), (3, 4), (4, 2), (5, 2), (0, 3), (1, 5)]
    knockout_idx = [(0, 2, 4), (1, 3, 5), (2, 3, 1), (3, 4, 0), (4, 1, 2), (5, 0, 3), (0, 5, 2), (1, 4, 5)]
    records = []

    def make(mode, floor_no, actual, names, mons, battle_type, opponent_index=None):
        suffix = "" if actual == "CHALLENGE_TYPE_SINGLE" else "_DOUBLES" if actual == "CHALLENGE_TYPE_DOUBLE" else "_KNOCKOUT"
        map_id = f"MAP_TRAINER_TOWER_{floor_no}F{suffix}"
        tid = f"TRAINER_TOWER_{mode.removeprefix('CHALLENGE_TYPE_')}_FLOOR_{floor_no}" + (f"_OPPONENT_{opponent_index + 1}" if opponent_index is not None else "")
        display_names = list(dict.fromkeys(names))
        records.append({"id": stable_id("battle", tid), "trainer_id": tid, "trainer_name_en": " & ".join(display_names), "trainer_class_id": "TRAINER_TOWER", "trainer_class_en": "Trainer Tower", "map_id": map_id, "area_id": map_by_const.get(map_id, {}).get("id"), "area_name_en": map_by_const.get(map_id, {}).get("name_en", human_map(map_id)), "coordinates": None, "mandatory": False, "battle_type": battle_type, "rematch_stage": 0, "party": mons, "trainer_items": [], "reward": "Tempo do desafio e prêmio do modo/piso; nível de cada oponente igual ao maior nível da equipe do jogador.", "availability": "optional", "source": source_ref("src/trainer_tower_sets.c"), "party_source": source_ref("src/trainer_tower_sets.c"), "level_rule_source": source_ref("src/trainer_tower.c", 988)})

    for mode, pointers in modes.items():
        for floor_idx, pointer in enumerate(pointers[:8]):
            floor_no = floor_idx + 1; data = floor_defs.get(pointer)
            if not data: continue
            actual = data["challenge"]; trainers = data["trainers"]
            if actual == "CHALLENGE_TYPE_SINGLE" and trainers:
                mons = [trainers[0]["mons"][i] for i in single_idx[floor_idx] if i < len(trainers[0]["mons"])]
                make(mode, floor_no, actual, [trainers[0]["name"]], mons, "trainer_tower_single")
            elif actual == "CHALLENGE_TYPE_DOUBLE" and len(trainers) >= 2:
                mons = [trainers[i]["mons"][double_idx[floor_idx][i]] for i in range(2) if double_idx[floor_idx][i] < len(trainers[i]["mons"])]
                make(mode, floor_no, actual, [trainers[0]["name"], trainers[1]["name"]], mons, "trainer_tower_double")
            elif actual == "CHALLENGE_TYPE_KNOCKOUT":
                for i, trainer in enumerate(trainers[:3]):
                    idx = knockout_idx[floor_idx][i]
                    if idx < len(trainer["mons"]): make(mode, floor_no, actual, [trainer["name"]], [trainer["mons"][idx]], "trainer_tower_knockout", i)
    return records


def load_shops(src: Path, map_by_const: dict, objects_by_script: dict, blocks: dict, item_meta: dict):
    shops = []
    for label, info in blocks.items():
        mart = re.search(r"\bpokemart\s+([A-Za-z0-9_]+)", info["text"])
        if not mart: continue
        stock_block = blocks.get(mart.group(1), {}).get("text", "")
        stock_ids = [x for x in re.findall(r"\.2byte\s+(ITEM_[A-Z0-9_]+)", stock_block) if x != "ITEM_NONE"]
        if not stock_ids: continue
        rel = str(info["path"].relative_to(src)).replace("\\", "/")
        map_id = None
        mm = re.match(r"data/maps/([^/]+)/", rel)
        if mm:
            p = src / "data/maps" / mm.group(1) / "map.json"
            if p.exists(): map_id = json.loads(read(p))["id"]
        coords = objects_by_script.get(label, [{}])[0]
        map_id = coords.get("map_id", map_id)
        condition = "Disponível ao falar com o vendedor."
        if "Expanded" in mart.group(1): condition = "Estoque expandido conforme o progresso da história de Two Island."
        shops.append({
            "id": stable_id("shop", label, mart.group(1)), "vendor_id": label, "stock_id": mart.group(1),
            "name_en": human_map(map_id) + " shop" if map_id else mart.group(1), "map_id": map_id,
            "area_id": map_by_const.get(map_id, {}).get("id"), "coordinates": {"x": coords.get("x"), "y": coords.get("y")} if coords.get("x") is not None else None,
            "condition": condition, "currency": "money", "availability": "normal",
            "stock": [{"item_id": x, "item_name_en": item_meta.get(x, {}).get("english", strip_const(x, "ITEM_")), "price": item_meta.get(x, {}).get("price")} for x in stock_ids],
            "source": source_ref(rel)
        })
    specials = [
        ("Celadon vending machines", "MAP_CELADON_CITY_DEPARTMENT_STORE_ROOF", "money", [("ITEM_FRESH_WATER", 200), ("ITEM_SODA_POP", 300), ("ITEM_LEMONADE", 350)], "CeladonCity_DepartmentStore_Roof/scripts.inc"),
        ("Game Corner Pokémon prizes", "MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM", "coins", [("SPECIES_ABRA", 180), ("SPECIES_CLEFAIRY", 500), ("SPECIES_DRATINI", 2800), ("SPECIES_SCYTHER", 5500), ("SPECIES_PORYGON", 9999)], "CeladonCity_GameCorner_PrizeRoom/scripts.inc"),
        ("Game Corner TM prizes", "MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM", "coins", [("ITEM_TM13", 4000), ("ITEM_TM23", 3500), ("ITEM_TM24", 4000), ("ITEM_TM30", 4500), ("ITEM_TM35", 4000)], "CeladonCity_GameCorner_PrizeRoom/scripts.inc"),
        ("Game Corner item prizes", "MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM", "coins", [("ITEM_SMOKE_BALL", 800), ("ITEM_MIRACLE_SEED", 1000), ("ITEM_CHARCOAL", 1000), ("ITEM_MYSTIC_WATER", 1000), ("ITEM_YELLOW_FLUTE", 1600)], "CeladonCity_GameCorner_PrizeRoom/scripts.inc"),
    ]
    for name, map_id, currency, stock, path in specials:
        shops.append({"id": stable_id("shop", name), "vendor_id": None, "stock_id": None, "name_en": name, "map_id": map_id, "area_id": map_by_const.get(map_id, {}).get("id"), "coordinates": None, "condition": "Coin Case exigido para prêmios do Game Corner." if currency == "coins" else "Disponível nas máquinas do telhado.", "currency": currency, "availability": "optional", "stock": [{"item_id": x, "item_name_en": item_meta.get(x, {}).get("english", strip_const(x, "ITEM_") if x.startswith("ITEM_") else strip_const(x, "SPECIES_")), "price": price} for x, price in stock], "source": source_ref("data/maps/" + path)})
    return shops


def load_special_encounters(src: Path, map_by_const: dict, objects_by_script: dict, blocks: dict):
    rows = []
    for path in sorted((src / "data/maps").glob("*/scripts.inc")):
        pmap = path.parent / "map.json"
        if not pmap.exists(): continue
        map_id = json.loads(read(pmap))["id"]
        text = read(path)
        for kind, pattern in (("static", r"\bsetwildbattle\s+(SPECIES_[A-Z0-9_]+),\s*(\d+)"), ("event", r"\bseteventmon\s+(SPECIES_[A-Z0-9_]+),\s*(\d+)"), ("gift", r"\bgivemon\s+(SPECIES_[A-Z0-9_]+),\s*(\d+)")):
            for m in re.finditer(pattern, text):
                availability = "event_required" if map_id.startswith(("MAP_BIRTH_ISLAND", "MAP_NAVEL_ROCK")) else "optional"
                rows.append({"id": stable_id("special", map_id, kind, m.group(1), m.group(2), m.start()), "map_id": map_id, "area_id": map_by_const.get(map_id, {}).get("id"), "area_name_en": map_by_const.get(map_id, {}).get("name_en", human_map(map_id)), "kind": kind, "species_id": m.group(1), "species": strip_const(m.group(1), "SPECIES_"), "level": int(m.group(2)), "conditions": "Interação/evento de mapa; consulte o capítulo correspondente.", "availability": availability, "source": source_ref(str(path.relative_to(src)).replace("\\", "/"))})
    def add_manual(map_id, kind, species_id, species, level, conditions, availability="optional", path="data/maps"):
        rows.append({"id": stable_id("special", map_id, kind, species_id), "map_id": map_id, "area_id": map_by_const.get(map_id, {}).get("id"), "area_name_en": map_by_const.get(map_id, {}).get("name_en", human_map(map_id)) if map_id else "Kanto routes", "kind": kind, "species_id": species_id, "species": species, "level": level, "conditions": conditions, "availability": availability, "source": source_ref(path)})
    for sid in ("SPECIES_BULBASAUR", "SPECIES_CHARMANDER", "SPECIES_SQUIRTLE"):
        add_manual("MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB", "starter_choice", sid, strip_const(sid, "SPECIES_"), 5, "Escolha exatamente um dos três starters.", path="data/maps/PalletTown_ProfessorOaksLab/scripts.inc")
    for sid in ("SPECIES_HITMONLEE", "SPECIES_HITMONCHAN"):
        add_manual("MAP_SAFFRON_CITY_DOJO", "gift_choice", sid, strip_const(sid, "SPECIES_"), 25, "Escolha exatamente um prêmio após vencer o Fighting Dojo.", path="data/maps/SaffronCity_Dojo/scripts.inc")
    for sid, level, coins in (("SPECIES_ABRA", 9, 180), ("SPECIES_CLEFAIRY", 8, 500), ("SPECIES_DRATINI", 18, 2800), ("SPECIES_SCYTHER", 25, 5500), ("SPECIES_PORYGON", 26, 9999)):
        add_manual("MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM", "prize", sid, strip_const(sid, "SPECIES_"), level, f"Troque {coins} coins no Game Corner; Coin Case exigido.", path="data/maps/CeladonCity_GameCorner_PrizeRoom/scripts.inc")
    add_manual("MAP_FIVE_ISLAND_WATER_LABYRINTH", "egg_gift", "SPECIES_TOGEPI", "Togepi", 5, "Receba o Egg com espaço na equipe e choque-o caminhando.", path="data/maps/FiveIsland_WaterLabyrinth/scripts.inc")
    rows.append({"id": stable_id("special", "roamer"), "map_id": None, "area_id": None, "area_name_en": "Kanto routes", "kind": "roaming", "species_id": "STARTER_DEPENDENT", "species": "Entei (Bulbasaur), Suicune (Charmander) ou Raikou (Squirtle)", "level": 50, "conditions": "National Pokédex e missão de Celio concluída; espécie definida pelo starter.", "availability": "optional", "source": source_ref("src/roamer.c")})
    return rows


def add_shop_item_sources(items: list, shops: list, map_by_const: dict):
    existing = {r["id"] for r in items}
    for shop in shops:
        for stock in shop["stock"]:
            item_id = stock["item_id"]
            if not item_id.startswith("ITEM_"): continue
            source_type = "prize" if shop["currency"] == "coins" else "shop"
            rid = stable_id("item", source_type, shop["id"], item_id)
            if rid in existing: continue
            existing.add(rid)
            map_id = shop.get("map_id")
            items.append({"id": rid, "item_id": item_id, "item_name_en": stock["item_name_en"], "source_type": source_type, "area_id": map_by_const.get(map_id, {}).get("id"), "map_id": map_id, "area_name_en": map_by_const.get(map_id, {}).get("name_en", human_map(map_id)) if map_id else None, "coordinates": shop.get("coordinates"), "directions_ptbr": f"Compre ou troque no ponto de venda {shop['name_en']}.", "quantity": 1, "renewable": True, "requirement": shop["condition"], "availability": shop["availability"], "price": stock["price"], "currency": shop["currency"], "script": shop.get("vendor_id"), "source": shop["source"]})


def load_trades(src: Path, map_by_const: dict):
    text = read(src / "src/data/ingame_trades.h")
    rows = []
    # FireRed preprocessor branches are retained by taking the first FIRERED value.
    for match, body in brace_blocks(text, r"\[(INGAME_TRADE_[A-Z0-9_]+)\]\s*=\s*\{"):
        tid = match.group(1)
        species = re.search(r"\.species\s*=\s*(SPECIES_[A-Z0-9_]+)", body)
        requested = re.search(r"(?:#if defined\(FIRERED\)[\s\S]*?)?\.requestedSpecies\s*=\s*(SPECIES_[A-Z0-9_]+)", body)
        nickname = re.search(r"\.nickname\s*=\s*_\(\"([^\"]+)\"\)", body)
        held = re.search(r"\.heldItem\s*=\s*(ITEM_[A-Z0-9_]+)", body)
        if species and requested:
            rows.append({"id": stable_id("trade", tid), "trade_id": tid, "receive_species_id": species.group(1), "receive_species": strip_const(species.group(1), "SPECIES_"), "requested_species_id": requested.group(1), "requested_species": strip_const(requested.group(1), "SPECIES_"), "nickname": nickname.group(1) if nickname else None, "held_item": held.group(1) if held else None, "map_id": None, "area_id": None, "availability": "trade_required", "source": source_ref("src/data/ingame_trades.h")})
    # Map trade constants to their NPC map.
    for path in (src / "data/maps").glob("*/scripts.inc"):
        pmap = path.parent / "map.json"
        if not pmap.exists(): continue
        content = read(path); map_id = json.loads(read(pmap))["id"]
        for row in rows:
            if row["trade_id"] in content: row["map_id"] = map_id; row["area_id"] = map_by_const.get(map_id, {}).get("id")
    return rows


def load_tutors(src: Path, map_by_const: dict, objects_by_script: dict, blocks: dict):
    text = read(src / "data/scripts/move_tutors.inc")
    rows = []
    for m in re.finditer(r"(?m)^([A-Za-z0-9_]*Tutor)::[\s\S]*?setvar VAR_0x8005, (MOVETUTOR_[A-Z0-9_]+)", text):
        label, tutor = m.group(1), m.group(2)
        locations = objects_by_script.get(label, [])
        if not locations:
            # Several map-local object scripts only jump to a shared tutor script.
            for alias, alias_locs in objects_by_script.items():
                if alias_locs and label in blocks.get(alias, {}).get("text", ""):
                    locations = alias_locs
                    break
        loc = (locations or [{}])[0]; map_id = loc.get("map_id")
        rows.append({"id": stable_id("tutor", label, tutor), "tutor_id": tutor, "move_en": strip_const(tutor, "MOVETUTOR_"), "map_id": map_id, "area_id": map_by_const.get(map_id, {}).get("id"), "coordinates": {"x": loc.get("x"), "y": loc.get("y")} if loc.get("x") is not None else None, "one_time": True, "availability": "optional", "source": source_ref("data/scripts/move_tutors.inc")})
    starter_label = "TwoIsland_CapeBrink_House_EventScript_StarterTutor"
    loc = objects_by_script.get(starter_label, [{}])[0]; map_id = loc.get("map_id")
    rows.append({"id": stable_id("tutor", starter_label, "ultimate-moves"), "tutor_id": "MOVETUTOR_STARTER_ULTIMATE", "move_en": "Frenzy Plant / Blast Burn / Hydro Cannon", "map_id": map_id, "area_id": map_by_const.get(map_id, {}).get("id"), "coordinates": {"x": loc.get("x"), "y": loc.get("y")} if loc.get("x") is not None else None, "one_time": False, "condition": "Somente o starter compatível com felicidade suficiente; cada ultimate move possui controle próprio.", "availability": "optional", "source": source_ref("data/scripts/move_tutors.inc")})
    return rows


def chapter_maps(chapter: dict, map_by_const: dict):
    def token(value: str) -> str:
        parts = []
        for part in value.split("_"):
            part = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", part)
            part = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", part)
            parts.append(part.upper())
        result = "_".join(parts)
        return {"SS_ANNE": "SSANNE"}.get(result, result)
    selected = []
    for map_id, area in map_by_const.items():
        raw = map_id.removeprefix("MAP_")
        for requested in chapter["areas"]:
            wanted = token(requested)
            if raw == wanted or raw.startswith(wanted + "_") or raw.endswith("_" + wanted) or ("_" + wanted + "_") in raw:
                selected.append(map_id)
                break
    return sorted(set(selected))


def frontmatter(meta: dict) -> str:
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            lines.extend(f"  - {json.dumps(x, ensure_ascii=False)}" for x in v)
        else: lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines)


def table(headers, rows):
    if not rows: return "_Nenhum registro desta categoria nesta etapa._"
    esc = lambda v: str(v if v is not None else "—").replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out.extend("| " + " | ".join(esc(v) for v in row) + " |" for row in rows)
    return "\n".join(out)


def render_chapters(out: Path, map_by_const, encounters, items, battles, shops, specials):
    chapter_index = []
    for ch in CHAPTERS:
        maps = chapter_maps(ch, map_by_const)
        entity_ids = [r["id"] for dataset in (encounters, items, battles, shops, specials) for r in dataset if r.get("map_id") in maps]
        meta = {"doc_id": f"walkthrough-{ch['number']:02d}", "game_version": VERSION, "sequence": ch["number"], "prerequisites": ch["prerequisites"], "areas": maps, "entity_ids": entity_ids, "tags": ["walkthrough", "firered", "pt-br"], "source_snapshot": SOURCE_COMMIT}
        lines = [frontmatter(meta), "", f"# {ch['number']:02d}. {ch['title']}", "", "## Estado inicial", "", ch["start"], "", "## Preparação recomendada", ""]
        lines += [f"- {x}" for x in ch["prep"]]
        lines += ["", "## Procedimento", ""] + [f"{i}. {x}" for i, x in enumerate(ch["actions"], 1)]
        enc = [r for r in encounters if r["map_id"] in maps]
        grouped = defaultdict(lambda: {"levels": set(), "rate": 0})
        for r in enc:
            method_label = r["method"] if r["encounter_variant"] == "default" else f"{r['method']} [{r['encounter_variant']}]"
            k = (r["area_name_en"], method_label, r["species"]); grouped[k]["levels"].add((r["min_level"], r["max_level"])); grouped[k]["rate"] = r["species_total_rate_percent"]
        enc_rows = []
        for (area, method, species), val in sorted(grouped.items()):
            levels = ", ".join(str(a) if a == b else f"{a}–{b}" for a, b in sorted(val["levels"]))
            enc_rows.append((area, method, species, levels, f"{val['rate']}%"))
        lines += ["", "## Encounters selvagens", "", table(["Área", "Método", "Pokémon", "Nível", "Taxa total"], enc_rows)]
        item_rows = [(r["area_name_en"], r["item_name_en"], r["source_type"], f"({r['coordinates']['x']}, {r['coordinates']['y']})" if r.get("coordinates") else "—", r["availability"]) for r in items if r.get("map_id") in maps]
        lines += ["", "## Itens", "", table(["Área", "Item", "Fonte", "Coordenadas", "Acesso"], item_rows)]
        battle_rows = []
        for r in battles:
            if r.get("map_id") not in maps: continue
            is_league_rematch = r.get("rematch_stage") == "league_round_2"
            if ch["number"] == 17 and is_league_rematch: continue
            if ch["number"] == 20 and r.get("map_id", "").startswith("MAP_POKEMON_LEAGUE_") and not is_league_rematch: continue
            party = "; ".join(f"{m['species']} Lv.{m['level']}" for m in r["party"])
            battle_rows.append((r["area_name_en"], f"{r['trainer_class_en']} {r['trainer_name_en']}", party, "obrigatória" if r["mandatory"] else "opcional", r["rematch_stage"]))
        lines += ["", "## Batalhas", "", table(["Área", "Treinador", "Equipe", "Categoria", "Rematch"], battle_rows)]
        shop_rows = [(human_map(r["map_id"]), r["name_en"], r["currency"], ", ".join(f"{s['item_name_en']} ({s['price']})" for s in r["stock"]), r["condition"]) for r in shops if r.get("map_id") in maps]
        lines += ["", "## Lojas e serviços", "", table(["Área", "Loja", "Moeda", "Estoque", "Condição"], shop_rows)]
        sp_rows = [(r["area_name_en"], r["kind"], r["species"], r["level"], r["availability"]) for r in specials if r.get("map_id") in maps or (ch["number"] == 20 and r["kind"] == "roaming")]
        lines += ["", "## Encontros fixos, gifts e eventos", "", table(["Área", "Tipo", "Pokémon", "Nível", "Acesso"], sp_rows)]
        lines += ["", "## Estratégia", "", f"> **Recomendação:** {ch['strategy']}", "", "## Bloqueios e revisitas", ""] + [f"- {x}" for x in ch["revisits"]]
        lines += ["", "## Estado final verificável", "", ch["end"], "", "## Proveniência", "", f"Dados estruturados: `pret/pokefirered@{SOURCE_COMMIT}`. Progressão redigida originalmente e conferida contra Bulbapedia e StrategyWiki."]
        path = out / "walkthrough" / f"{ch['number']:02d}-{ch['slug']}.md"
        write(path, "\n".join(lines)); chapter_index.append((ch["number"], ch["title"], path.name, len(entity_ids)))
    return chapter_index


def render_references(out: Path, datasets: dict):
    specs = {
        "areas": ("Índice de áreas", ["Nome", "Map ID", "Tipo", "Flash"], lambda r: (r["name_en"], r["map_id"], r["map_type"], r["requires_flash"])),
        "encounters": ("Índice de encounters", ["Área", "Método", "Pokémon", "Nível", "Slot", "Total"], lambda r: (r["area_name_en"], r["method"], r["species"], f"{r['min_level']}–{r['max_level']}", f"{r['slot_rate_percent']}%", f"{r['species_total_rate_percent']}%")),
        "battles": ("Índice de treinadores e batalhas", ["Área", "Treinador", "Equipe", "Rematch", "ID"], lambda r: (r.get("area_name_en"), f"{r['trainer_class_en']} {r['trainer_name_en']}", "; ".join(f"{m['species']} Lv.{m['level']}" for m in r["party"]), r["rematch_stage"], r["trainer_id"])),
        "items": ("Índice de fontes de itens", ["Área", "Item", "Fonte", "Posição", "Acesso"], lambda r: (r.get("area_name_en"), r["item_name_en"], r["source_type"], f"({r['coordinates']['x']}, {r['coordinates']['y']})" if r.get("coordinates") else "—", r["availability"])),
        "shops": ("Índice de lojas", ["Área", "Loja", "Moeda", "Itens"], lambda r: (human_map(r["map_id"]), r["name_en"], r["currency"], ", ".join(f"{s['item_name_en']} ({s['price']})" for s in r["stock"]))),
        "special_encounters": ("Encontros fixos e gifts", ["Área", "Tipo", "Pokémon", "Nível", "Acesso"], lambda r: (r["area_name_en"], r["kind"], r["species"], r["level"], r["availability"])),
        "trades": ("In-game trades", ["Local", "Entregar", "Receber", "Nickname", "Held item"], lambda r: (human_map(r["map_id"]) if r.get("map_id") else "Local no script não resolvido", r["requested_species"], r["receive_species"], r["nickname"], r["held_item"])),
        "tutors": ("Move Tutors", ["Local", "Move", "Posição", "Uso"], lambda r: (human_map(r["map_id"]) if r.get("map_id") else "Evento global", r["move_en"], f"({r['coordinates']['x']}, {r['coordinates']['y']})" if r.get("coordinates") else "—", "uma vez" if r["one_time"] else "repetível")),
    }
    for key, (title, headers, rowfn) in specs.items():
        rows = [rowfn(r) for r in datasets[key]]
        meta = frontmatter({"doc_id": f"reference-{key}", "game_version": VERSION, "tags": ["reference", key, "firered"], "source_snapshot": SOURCE_COMMIT})
        write(out / "reference" / f"{key}.md", f"{meta}\n\n# {title}\n\nRegistros canônicos: `data/{key}.json`.\n\n{table(headers, rows)}")

    # Entity-specific convenience references requested in the plan.
    pokemon = defaultdict(lambda: {"encounters": [], "special": [], "trades": []})
    for r in datasets["encounters"]: pokemon[r["species"]]["encounters"].append(r)
    for r in datasets["special_encounters"]: pokemon[r["species"]]["special"].append(r)
    for r in datasets["trades"]: pokemon[r["receive_species"]]["trades"].append(r)
    prows = []
    for species, data in sorted(pokemon.items()):
        areas = sorted({r["area_name_en"] for r in data["encounters"]} | {r["area_name_en"] for r in data["special"]})
        prows.append((species, ", ".join(areas) or "trade", len(data["encounters"]), len(data["special"]), len(data["trades"])))
    write(out / "reference/pokemon.md", f"{frontmatter({'doc_id':'reference-pokemon','game_version':VERSION,'tags':['reference','pokemon'],'source_snapshot':SOURCE_COMMIT})}\n\n# Índice por Pokémon\n\n{table(['Pokémon','Áreas','Slots selvagens','Fixos/gifts','Trades'], prows)}")

    tm_items = [r for r in datasets["items"] if r["item_id"].startswith(("ITEM_TM", "ITEM_HM"))]
    tm_shop = []
    for s in datasets["shops"]:
        for stock in s["stock"]:
            if stock["item_id"].startswith(("ITEM_TM", "ITEM_HM")): tm_shop.append((human_map(s["map_id"]), stock["item_name_en"], "shop/prize", stock["price"]))
    tm_rows = [(r.get("area_name_en"), r["item_name_en"], r["source_type"], r.get("requirement")) for r in tm_items] + tm_shop
    write(out / "reference/tm-hm.md", f"{frontmatter({'doc_id':'reference-tm-hm','game_version':VERSION,'tags':['reference','tm','hm'],'source_snapshot':SOURCE_COMMIT})}\n\n# TMs e HMs\n\n{table(['Área','Item','Fonte','Condição/preço'], tm_rows)}")

    event_rows = [(r["area_name_en"], r["species"], r["level"], r["availability"], r["conditions"]) for r in datasets["special_encounters"] if r["availability"] in {"event_required", "unavailable_normally", "version_specific"}]
    event_rows += [("Altering Cave", "Outros pools distribuídos", "—", "unavailable_normally", "A ROM GBA comum mantém apenas o pool padrão sem distribuição externa.")]
    write(out / "reference/events.md", f"{frontmatter({'doc_id':'reference-events','game_version':VERSION,'tags':['reference','events'],'source_snapshot':SOURCE_COMMIT})}\n\n# Eventos e dependências externas\n\n{table(['Área','Conteúdo','Nível','Acesso','Condição'], event_rows)}")

    coverage_rows = []
    for r in datasets["areas"]:
        chapters = r.get("walkthrough_chapters", [])
        reason = "Coberto diretamente no walkthrough." if chapters else "Mapa técnico, interior auxiliar ou área de sistema mantida no índice; não exige etapa sequencial própria."
        coverage_rows.append((r["name_en"], r["map_id"], ", ".join(f"{n:02d}" for n in chapters) or "reference-only", reason))
    write(out / "reference/map-coverage.md", f"{frontmatter({'doc_id':'reference-map-coverage','game_version':VERSION,'tags':['reference','maps','coverage'],'source_snapshot':SOURCE_COMMIT})}\n\n# Cobertura dos mapas\n\n{table(['Área','Map ID','Capítulos','Justificativa'], coverage_rows)}")


def schemas():
    base_source = {"type": "object", "required": ["repository", "commit", "path"], "properties": {"repository": {"type": "string"}, "commit": {"type": "string"}, "path": {"type": "string"}, "line": {"type": ["integer", "null"]}}}
    def schema(required, props):
        common = {"id": {"type": "string"}, "availability": {"enum": sorted(AVAILABILITY)}, "source": base_source}
        common.update(props)
        return {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "array", "items": {"type": "object", "required": ["id"] + required, "properties": common}}
    return {
        "areas": schema(["map_id", "name_en", "source"], {"map_id": {"type": "string"}, "name_en": {"type": "string"}}),
        "encounters": schema(["map_id", "method", "species_id", "min_level", "max_level", "slot_rate_percent", "availability", "source"], {"map_id": {"type": "string"}, "method": {"enum": ["land", "surf", "rock_smash", "old_rod", "good_rod", "super_rod"]}, "species_id": {"type": "string"}, "min_level": {"type": "integer"}, "max_level": {"type": "integer"}, "slot_rate_percent": {"type": "integer"}}),
        "items": schema(["item_id", "source_type", "availability", "source"], {"item_id": {"type": "string"}, "source_type": {"enum": ["visible", "hidden", "gift", "prize", "shop", "held"]}}),
        "battles": schema(["trainer_id", "trainer_name_en", "party", "availability", "source"], {"trainer_id": {"type": "string"}, "trainer_name_en": {"type": "string"}, "party": {"type": "array", "minItems": 1}}),
        "shops": schema(["name_en", "stock", "availability", "source"], {"name_en": {"type": "string"}, "stock": {"type": "array", "minItems": 1}}),
        "special_encounters": schema(["kind", "species", "level", "availability", "source"], {"kind": {"type": "string"}, "species": {"type": "string"}, "level": {"type": "integer"}}),
        "trades": schema(["receive_species_id", "requested_species_id", "availability", "source"], {"receive_species_id": {"type": "string"}, "requested_species_id": {"type": "string"}}),
        "tutors": schema(["tutor_id", "move_en", "availability", "source"], {"tutor_id": {"type": "string"}, "move_en": {"type": "string"}}),
    }


def validate(datasets: dict, map_by_const: dict, out: Path):
    errors, warnings = [], []
    all_ids = []
    for name, rows in datasets.items():
        ids = [r.get("id") for r in rows]
        if None in ids: errors.append(f"{name}: registro sem id")
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        if dupes: errors.append(f"{name}: IDs duplicados: {dupes[:5]}")
        all_ids.extend(ids)
        for r in rows:
            if "availability" in r and r["availability"] not in AVAILABILITY: errors.append(f"{name}/{r['id']}: availability inválida")
            if r.get("map_id") and r["map_id"] not in map_by_const: warnings.append(f"{name}/{r['id']}: mapa sem map.json: {r['map_id']}")
            if r.get("source") and r["source"].get("commit") != SOURCE_COMMIT: errors.append(f"{name}/{r['id']}: commit incorreto")
    required = {
        "areas": ["id", "map_id", "name_en", "source"],
        "encounters": ["id", "map_id", "method", "species_id", "min_level", "max_level", "slot_rate_percent", "availability", "source"],
        "items": ["id", "item_id", "source_type", "availability", "source"],
        "battles": ["id", "trainer_id", "trainer_name_en", "party", "availability", "source"],
        "shops": ["id", "name_en", "stock", "availability", "source"],
        "special_encounters": ["id", "kind", "species", "level", "availability", "source"],
        "trades": ["id", "receive_species_id", "requested_species_id", "availability", "source"],
        "tutors": ["id", "tutor_id", "move_en", "availability", "source"],
    }
    for name, fields in required.items():
        for r in datasets[name]:
            missing = [f for f in fields if f not in r or r[f] is None or r[f] == ""]
            if missing: errors.append(f"{name}/{r.get('id')}: campos obrigatórios ausentes: {missing}")
    for r in datasets["encounters"]:
        if not (0 < r["slot_rate_percent"] <= 100): errors.append(f"Taxa inválida: {r['id']}")
    sums = defaultdict(int)
    for r in datasets["encounters"]: sums[(r["encounter_table_id"], r["method"])] += r["slot_rate_percent"]
    for key, total in sums.items():
        if total != 100: errors.append(f"Slots de encounter não somam 100: {key}={total}")
    for ch in CHAPTERS:
        if not ch["start"] or not ch["actions"] or not ch["end"]: errors.append(f"Capítulo {ch['number']} sem contrato de estado")
    # Acceptance queries are evaluated against the canonical data, not just listed.
    route3 = {species: next(x["species_total_rate_percent"] for x in datasets["encounters"] if x["map_id"] == "MAP_ROUTE3" and x["species"] == species) for species in ("Spearow", "Pidgey", "Mankey", "Jigglypuff")}
    if route3 != {"Spearow": 35, "Pidgey": 30, "Mankey": 10, "Jigglypuff": 10}: errors.append(f"Consulta Route 3 divergente: {route3}")
    mansion_hidden = [x for x in datasets["items"] if (x.get("map_id") or "").startswith("MAP_POKEMON_MANSION") and x["source_type"] == "hidden"]
    if not mansion_hidden: errors.append("Consulta Pokémon Mansion sem hidden items")
    rival_variants = [x for x in datasets["battles"] if x["trainer_id"].startswith("TRAINER_RIVAL_")]
    if len(rival_variants) < 3: errors.append("Variantes do rival incompletas")
    required_events = {x["species"] for x in datasets["special_encounters"] if x["availability"] == "event_required"}
    if not {"Deoxys", "Lugia", "Ho Oh"}.issubset(required_events): errors.append(f"Eventos de ticket incompletos: {required_events}")
    brock = next((x for x in datasets["battles"] if x["trainer_id"] == "TRAINER_LEADER_BROCK"), None)
    if not brock or [(m["species"], m["level"]) for m in brock["party"]] != [("Geodude", 12), ("Onix", 14)]: errors.append("Equipe de Brock divergente")
    md_files = list(out.rglob("*.md"))
    for p in md_files:
        text = read(p)
        if "TODO" in text or "TBD" in text: errors.append(f"Placeholder em {p.relative_to(out)}")
        if not text.startswith("---\n"): errors.append(f"Markdown sem front matter: {p.relative_to(out)}")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"): continue
            resolved = (p.parent / target).resolve()
            if not resolved.exists(): errors.append(f"Link quebrado em {p.relative_to(out)}: {target}")
    report = {
        "status": "PASS" if not errors else "FAIL", "source_commit": SOURCE_COMMIT, "rom_sha1": ROM_SHA1,
        "counts": {k: len(v) for k, v in datasets.items()}, "walkthrough_chapters": len(CHAPTERS), "markdown_files": len(md_files),
        "encounter_tables": len(sums), "errors": errors, "warnings": warnings,
        "representative_queries": [
            {"query": "Quais encontros existem em Route 3 e suas taxas?", "answer_locations": ["walkthrough/04-route-3-mt-moon-route-4.md", "reference/encounters.md"]},
            {"query": "O que devo fazer depois de obter Surf?", "answer_locations": ["walkthrough/10-routes-12-18-fuchsia.md", "walkthrough/12-routes-19-20-seafoam.md"]},
            {"query": "Quais itens ocultos ainda posso pegar em Pokémon Mansion?", "answer_locations": ["walkthrough/13-cinnabar-mansion-gym.md", "reference/items.md"]},
            {"query": "Qual é a equipe do próximo rival para meu starter?", "answer_locations": ["reference/battles.md"]},
            {"query": "O que exige Mystery Gift, trade ou outro jogo?", "answer_locations": ["reference/events.md", "reference/trades.md"]},
        ]
    }
    dump(out / "qa/validation-report.json", report)
    write(out / "qa/VALIDATION.md", frontmatter({"doc_id": "qa-validation", "game_version": VERSION, "tags": ["qa", "validation"], "source_snapshot": SOURCE_COMMIT}) + f"\n\n# Relatório de validação\n\n**Status:** {report['status']}\n\n**Commit:** `{SOURCE_COMMIT}`\n\n**Contagens:**\n\n" + "\n".join(f"- {k}: {v}" for k, v in report["counts"].items()) + f"\n- capítulos: {len(CHAPTERS)}\n- arquivos Markdown: {len(md_files)}\n\n## Erros\n\n" + ("\n".join(f"- {e}" for e in errors) or "Nenhum.") + "\n\n## Avisos\n\n" + ("\n".join(f"- {w}" for w in warnings) or "Nenhum."))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="Checkout do pret/pokefirered no commit fixado")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(); src = args.source.resolve(); out = args.output.resolve()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=src, text=True).strip()
    if commit != SOURCE_COMMIT: raise SystemExit(f"Fonte incorreta: esperado {SOURCE_COMMIT}, recebido {commit}")
    for folder in ("data", "schemas", "walkthrough", "reference", "qa"):
        p = out / folder
        if p.exists(): shutil.rmtree(p)
        p.mkdir(parents=True)
    areas, map_by_const, objects_by_script = load_maps(src)
    blocks = collect_script_blocks(src)
    encounters = load_encounters(src, map_by_const)
    items, item_meta = load_items(src, map_by_const, objects_by_script, blocks, encounters)
    battles = load_trainers(src, map_by_const, objects_by_script, blocks)
    battles.extend(load_trainer_tower(src, map_by_const))
    battles.sort(key=lambda r: (r.get("map_id") or "ZZZ", r["trainer_id"]))
    shops = load_shops(src, map_by_const, objects_by_script, blocks, item_meta)
    add_shop_item_sources(items, shops, map_by_const)
    special = load_special_encounters(src, map_by_const, objects_by_script, blocks)
    trades = load_trades(src, map_by_const)
    tutors = load_tutors(src, map_by_const, objects_by_script, blocks)
    datasets = {"areas": areas, "encounters": encounters, "items": items, "battles": battles, "shops": shops, "special_encounters": special, "trades": trades, "tutors": tutors}
    for ch in CHAPTERS:
        for map_id in chapter_maps(ch, map_by_const):
            map_by_const[map_id].setdefault("walkthrough_chapters", []).append(ch["number"])
    for name, rows in datasets.items(): dump(out / "data" / f"{name}.json", rows)
    for name, doc in schemas().items(): dump(out / "schemas" / f"{name}.schema.json", doc)
    chapter_index = render_chapters(out, map_by_const, encounters, items, battles, shops, special)
    render_references(out, datasets)
    manifest = {"game_version": VERSION, "language": "pt-BR with canonical English entity names", "source_repository": "https://github.com/pret/pokefirered", "source_commit": SOURCE_COMMIT, "rom_sha1": ROM_SHA1, "secondary_sources": [{"name": "Bulbapedia walkthrough", "url": "https://bulbapedia.bulbagarden.net/wiki/Walkthrough:Pok%C3%A9mon_FireRed_and_LeafGreen", "use": "progression cross-check"}, {"name": "StrategyWiki walkthrough", "url": "https://strategywiki.org/wiki/Pok%C3%A9mon_FireRed_and_LeafGreen/Walkthrough", "use": "area-order cross-check"}]}
    dump(out / "data/source-manifest.json", manifest)
    readme = f"""{frontmatter({'doc_id':'readme','game_version':VERSION,'tags':['index','firered','ai-guide'],'source_snapshot':SOURCE_COMMIT})}

# Pokémon FireRed AI Guide

Base modular em PT-BR para Pokémon FireRed GBA USA v1.0. Nomes de Pokémon, moves, items, abilities e locations permanecem em inglês.

## Comece aqui

1. Um agente deve ler `AGENT_GUIDE.md`.
2. Para conduzir uma partida, abra o capítulo correto em `walkthrough/`.
3. Para perguntas pontuais, consulte `reference/`.
4. Para cálculos ou automação, trate `data/` como fonte canônica; Markdown é uma visualização gerada.

## Cobertura

- 21 capítulos: história, conteúdo opcional, Sevii Islands, pós-game, Cerulean Cave, League Round 2 e eventos.
- Encounters por método, nível, slot e taxa agregada.
- Item balls, hidden items, NPC gifts, lojas, Game Corner e vending machines.
- Batalhas regulares, chefes, variantes do rival e VS Seeker/rematches presentes nos scripts.
- Fixed encounters, gifts, in-game trades e Move Tutors.

## Autoridade e proveniência

- Fonte técnica fixada: `pret/pokefirered@{SOURCE_COMMIT}`.
- SHA-1 da ROM de referência: `{ROM_SHA1}`.
- Bulbapedia e StrategyWiki são usadas apenas para conferir progressão. A redação é original.
- FireRed v1.1 e Switch não são autoridades deste pacote.

## Arquivos

| Pasta | Uso |
| --- | --- |
| `walkthrough/` | sequência jogável com estados verificáveis |
| `reference/` | consulta humana/semântica por entidade |
| `data/` | registros JSON canônicos |
| `schemas/` | contratos dos registros |
| `tools/` | regeneração e validação |
| `qa/` | relatório de auditoria |

## Regeneração

```powershell
python tools/build_guide.py --source <checkout-pokefirered-no-commit-fixado> --output .
```

O gerador aborta se o checkout não estiver exatamente no commit fixado.

## Capítulos

{chr(10).join(f'- [{n:02d}. {title}](walkthrough/{file}) — {count} entidades relacionadas' for n, title, file, count in chapter_index)}
"""
    write(out / "README.md", readme)
    agent = f"""{frontmatter({'doc_id':'agent-guide','game_version':VERSION,'tags':['agent-contract','firered'],'source_snapshot':SOURCE_COMMIT})}

# Contrato para agentes de IA

## Ordem de autoridade

1. `data/*.json`: fatos extraídos do jogo.
2. `walkthrough/*.md`: ordem operacional e estados.
3. `reference/*.md`: visualizações para consulta.
4. Blocos **Recomendação**: estratégia opinativa, nunca regra do jogo.

## Resolução de consultas

- Identifique a versão. Este pacote responde por **{VERSION}**.
- Determine o estado: Badges, Key Items, capítulo, starter, Pokémon capturados e eventos únicos já resolvidos.
- Consulte o capítulo da visita atual. Áreas revisitadas podem ter pré-requisitos diferentes.
- Use IDs e `map_id` para cruzar encounters, itens, batalhas e lojas.
- Ao responder taxas, some apenas slots do mesmo `map_id`, método e espécie; o campo `species_total_rate_percent` já contém esse total.
- Nunca apresente `event_required`, `trade_required` ou `unavailable_normally` como obtenção normal.

## Estado mínimo recomendado

```json
{{
  "chapter": 1,
  "location_map_id": "MAP_PALLET_TOWN",
  "starter": null,
  "badges": [],
  "key_items": [],
  "captured_species": [],
  "resolved_unique_encounters": [],
  "story_flags_summary": []
}}
```

## Política de navegação

- Direções naturais orientam humanos.
- `map_id` e coordenadas `(x, y)` são a referência determinística.
- Coordenadas ausentes significam que o evento é global, móvel ou não está ligado a um object event único; não invente posição.

## Fato versus recomendação

- Fato: possui `source.repository`, `source.commit` e `source.path`.
- Recomendação: aparece explicitamente em bloco rotulado e pode variar conforme a equipe.
- Se duas fontes secundárias divergirem, prefira o dado técnico do commit fixado e registre a divergência.

## Acesso externo

- `trade_required`: troca com NPC ou outro jogo, conforme o registro.
- `event_required`: ticket/distribuição externa.
- `unavailable_normally`: conteúdo presente nos dados mas não liberado numa partida GBA comum.
- `version_specific`: válido apenas na variante declarada.
"""
    write(out / "AGENT_GUIDE.md", agent)
    audit = f"""{frontmatter({'doc_id':'qa-cross-source-audit','game_version':VERSION,'tags':['qa','cross-source'],'source_snapshot':SOURCE_COMMIT})}

# Auditoria cruzada por amostragem

Os dados técnicos abaixo foram extraídos do commit fixado. As fontes secundárias servem somente para detectar divergências de leitura ou progressão.

| Amostra | Resultado técnico | Segunda fonte | Resultado |
| --- | --- | --- | --- |
| Route 3 encounters | Spearow 35%, Pidgey 30%, Mankey 10%, Nidoran M 14%, Jigglypuff 10%, Nidoran F 1% | https://bulbapedia.bulbagarden.net/wiki/Kanto_Route_3 | Compatível com a tabela FRLG; nenhuma divergência aberta. |
| Brock | Geodude Lv.12; Onix Lv.14 | https://bulbapedia.bulbagarden.net/wiki/Brock_(game) | Compatível. |
| Viridian Mart | Poké Ball 200, Potion 300, Antidote 100, Parlyz Heal 200 | https://strategywiki.org/wiki/Pok%C3%A9mon_FireRed_and_LeafGreen/Viridian_City | Compatível. |
| Pokémon Mansion | Secret Key no B1F; quatro pisos; itens visíveis e ocultos separados | https://bulbapedia.bulbagarden.net/wiki/Pokemon_Mansion_(Kanto) | Compatível com a progressão e a separação por piso. |
| Itens falsos na Power Plant | Dois Electrode Lv.34 registrados como encontros fixos, não itens | https://bulbapedia.bulbagarden.net/wiki/Hidden_item | Compatível com a observação sobre item balls disfarçados. |

## Política de divergência

Se uma futura versão das fontes secundárias divergir, `data/*.json` continua obedecendo ao commit técnico fixado. A divergência deve ser adicionada a esta tabela antes de qualquer alteração factual.
"""
    write(out / "qa/CROSS_SOURCE_AUDIT.md", audit)
    report = validate(datasets, map_by_const, out)
    if report["status"] != "PASS": raise SystemExit("Validação falhou; consulte qa/validation-report.json")
    print(json.dumps(report["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
