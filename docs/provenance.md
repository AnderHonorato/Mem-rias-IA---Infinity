# Proveniência

O modelo é inspirado em W3C PROV: **Entity**, **Activity** e **Agent**, sem exigir RDF.

Cada registro importante deve conseguir apontar, quando disponível:

- quem afirmou ou produziu;
- quando ocorreu/foi registrado;
- origem (`source.type` e `source.ref`);
- agente que gerou (`generated_by.agent`);
- derivação (`derived_from`);
- atribuição (`attributed_to`);
- evidências;
- confirmação;
- registro anterior que substitui ou pelo qual foi substituído.

Relações são referências por ID estável. Referência quebrada deve falhar nos checks ou ser sinalizada para revisão.
