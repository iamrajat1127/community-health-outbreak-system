// import React, { useEffect, useState } from "react";
// import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

// function colorFromIntensity(intensity) {
//   if (intensity === "red") return "red";
//   if (intensity === "orange") return "orange";
//   if (intensity === "yellow") return "gold";
//   return "green";
// }

// export default function OutbreakMap() {
//   const [data, setData] = useState([]);

//   useEffect(() => {
//     fetch("/map_outbreaks.json")
//       .then((res) => res.json())
//       .then((json) => setData(json));
//   }, []);

//   return (
//     <MapContainer
//       center={[22.5937, 78.9629]}
//       zoom={5}
//       style={{ height: "90vh", width: "100%" }}
//     >
//       <TileLayer
//         attribution="&copy; OpenStreetMap contributors"
//         url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//       />

//       {data.map((r, idx) => (
//         <CircleMarker
//           key={idx}
//           center={[Number(r.lat), Number(r.lon)]}
//           radius={8}
//           pathOptions={{
//             color: colorFromIntensity(r.intensity),
//             fillColor: colorFromIntensity(r.intensity),
//             fillOpacity: 0.8,
//           }}
//         >
//           <Popup>
//             <b>
//               {r.city}, {r.state}
//             </b>
//             <div>Date: {r.date}</div>
//             <div>Z-score: {Number(r.z_score).toFixed(2)}</div>
//             <div>Intensity: {r.intensity}</div>
//             <div>Symptoms: {Number(r.weighted_symptoms).toFixed(2)}</div>
//             <div>Diseases: {Number(r.weighted_diseases).toFixed(2)}</div>
//           </Popup>
//         </CircleMarker>
//       ))}
//     </MapContainer>
//   );
// }

////////////////////////////////////////////////////////////////////////////////////////////////////

// import React, { useEffect, useState, useMemo } from "react";
// import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

// function colorFromIntensity(intensity) {
//   if (intensity === "red") return "red";
//   if (intensity === "orange") return "orange";
//   if (intensity === "yellow") return "gold";
//   return "green";
// }

// export default function OutbreakMap() {
//   const [data, setData] = useState([]);
//   const [explanations, setExplanations] = useState({});
//   const [selected, setSelected] = useState(null);
//   const [tips, setTips] = useState({});

//   useEffect(() => {
//     fetch("/map_outbreaks.json")
//       .then((res) => res.json())
//       .then((json) => setData(json))
//       .catch((e) => console.error("Failed loading map_outbreaks.json", e));

//     fetch("/city_date_explanations.json")
//       .then((res) => res.json())
//       .then((json) => setExplanations(json))
//       .catch((e) => console.error("Failed loading city_date_explanations.json", e));

//     fetch("/health_tips.json")
//       .then((res) => res.json())
//       .then((json) => setTips(json))
//       .catch((e) => console.error("Failed loading health_tips.json", e));
//   }, []);

//   const selectedKey = useMemo(() => {
//     if (!selected) return null;
//     const city = String(selected.city).trim().toLowerCase();
//     const state = String(selected.state).trim().toLowerCase();
//     const date = String(selected.date);
//     return `${city}|${state}|${date}`;
//   }, [selected]);

//   const explain = selectedKey ? explanations[selectedKey] : null;

//   const topDisease = useMemo(() => {
//   if (!explain || !explain.top_diseases || explain.top_diseases.length === 0) return null;
//   return explain.top_diseases[0][0]; // disease name string
//   }, [explain]);

//   const selectedTip = topDisease ? tips[topDisease] : null;

//   return (
//     <div style={{ display: "flex", height: "90vh", gap: "12px" }}>
//       {/* Map */}
//       <div style={{ flex: 3, borderRadius: "12px", overflow: "hidden" }}>
//         <MapContainer
//           center={[22.5937, 78.9629]}
//           zoom={5}
//           style={{ height: "100%", width: "100%" }}
//         >
//           <TileLayer
//             attribution="&copy; OpenStreetMap contributors"
//             url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//           />

//           {data.map((r, idx) => (
//             <CircleMarker
//               key={idx}
//               center={[Number(r.lat), Number(r.lon)]}
//               radius={8}
//               pathOptions={{
//                 color: colorFromIntensity(r.intensity),
//                 fillColor: colorFromIntensity(r.intensity),
//                 fillOpacity: 0.8,
//               }}
//               eventHandlers={{
//                 click: () => setSelected(r),
//               }}
//             >
//               <Popup>
//                 <b>
//                   {r.city}, {r.state}
//                 </b>
//                 <div>Date: {r.date}</div>
//                 <div>Z-score: {Number(r.z_score).toFixed(2)}</div>
//                 <div>Intensity: {r.intensity}</div>
//               </Popup>
//             </CircleMarker>
//           ))}
//         </MapContainer>
//       </div>

//       {/* Explainability Panel */}
//       <div style={{ flex: 1, border: "1px solid #ddd", borderRadius: "12px", padding: "12px", overflowY: "auto" }}>
//         <h3 style={{ marginTop: 0 }}>Why flagged?</h3>

//         {!selected ? (
//           <p>Click a city marker to see explanation.</p>
//         ) : (
//           <>
//             <h4 style={{ marginBottom: "6px" }}>
//               {selected.city}, {selected.state}
//             </h4>
//             <div><b>Date:</b> {selected.date}</div>
//             <div><b>Z-score:</b> {Number(selected.z_score).toFixed(2)}</div>
//             <div><b>Intensity:</b> {selected.intensity}</div>

//             <hr />

//             {!explain ? (
//               <p>Loading explanation...</p>
//             ) : (
//               <>
//                 {explain.note ? (
//                   <p>{explain.note}</p>
//                 ) : (
//                   <>
//                     <div style={{ marginBottom: "10px" }}>
//                       <b>Top symptoms</b>
//                       {explain.top_symptoms?.length ? (
//                         <ul>
//                           {explain.top_symptoms.map(([name, val], i) => (
//                             <li key={i}>
//                               {name} — {val.toFixed(2)}
//                             </li>
//                           ))}
//                         </ul>
//                       ) : (
//                         <p>No symptom signals found.</p>
//                       )}
//                     </div>

//                     <div style={{ marginBottom: "10px" }}>
//                       <b>Top disease mentions</b>
//                       {explain.top_diseases?.length ? (
//                         <ul>
//                           {explain.top_diseases.map(([name, val], i) => (
//                             <li key={i}>
//                               {name} — {val.toFixed(2)}
//                             </li>
//                           ))}
//                         </ul>
//                       ) : (
//                         <p>No disease mentions found.</p>
//                       )}
//                     </div>

//                     <div>
//                       <b>Sample community messages</b>
//                       {explain.sample_messages?.length ? (
//                         <ul>
//                           {explain.sample_messages.map((m, i) => (
//                             <li key={i} style={{ marginBottom: "6px" }}>
//                               {m}
//                             </li>
//                           ))}
//                         </ul>
//                       ) : (
//                         <p>No sample messages.</p>
//                       )}
//                     </div>
//                   </>
//                 )}
//               </>
//             )}
//           </>
//         )}
//       </div>
//     </div>
//   );
// }

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// FULL FINAL CODE (map + right panel + tips)
import React, { useEffect, useState, useMemo } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

function colorFromIntensity(intensity) {
  if (intensity === "red") return "red";
  if (intensity === "orange") return "orange";
  if (intensity === "yellow") return "gold";
  return "green";
}

export default function OutbreakMap() {
  const [data, setData] = useState([]);
  const [explanations, setExplanations] = useState({});
  const [tips, setTips] = useState({});
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("/map_outbreaks.json").then(r => r.json()).then(setData);
    fetch("/city_date_explanations.json").then(r => r.json()).then(setExplanations);
    fetch("/health_tips.json").then(r => r.json()).then(setTips);
  }, []);

  const selectedKey = useMemo(() => {
    if (!selected) return null;
    return `${selected.city.toLowerCase()}|${selected.state.toLowerCase()}|${selected.date}`;
  }, [selected]);

  const explain = selectedKey ? explanations[selectedKey] : null;

  const topDisease = useMemo(() => {
    if (!explain || !explain.top_diseases?.length) return null;
    return explain.top_diseases[0][0];
  }, [explain]);

  const selectedTip = topDisease ? tips[topDisease] : null;

  return (
    <div style={{ display: "flex", height: "90vh" }}>
      {/* MAP */}
      <div style={{ flex: 3 }}>
        <MapContainer
          center={[22.5937, 78.9629]}
          zoom={5}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {data.map((r, idx) => (
            <CircleMarker
              key={idx}
              center={[Number(r.lat), Number(r.lon)]}
              radius={8}
              pathOptions={{
                color: colorFromIntensity(r.intensity),
                fillColor: colorFromIntensity(r.intensity),
                fillOpacity: 0.8,
              }}
              eventHandlers={{ click: () => setSelected(r) }}
            >
              <Popup>
                <b>{r.city}, {r.state}</b><br/>
                Z: {Number(r.z_score).toFixed(2)}
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      {/* RIGHT PANEL */}
      <div style={{ flex: 2, padding: "15px", overflowY: "auto", borderLeft: "1px solid #ddd" }}>
        {!selected ? (
          <h3>Click a city to see outbreak details</h3>
        ) : (
          <>
            <h2>{selected.city}, {selected.state}</h2>
            <p><b>Date:</b> {selected.date}</p>

            <h3>Why flagged?</h3>
            {explain && (
              <>
                <b>Top Symptoms</b>
                <ul>
                  {explain.top_symptoms.map(([s,v],i)=>(
                    <li key={i}>{s} — {v.toFixed(2)}</li>
                  ))}
                </ul>

                <b>Top Diseases</b>
                <ul>
                  {explain.top_diseases.map(([d,v],i)=>(
                    <li key={i}>{d} — {v.toFixed(2)}</li>
                  ))}
                </ul>

                <b>Sample Messages</b>
                <ul>
                  {explain.sample_messages.map((m,i)=>(
                    <li key={i}>{m}</li>
                  ))}
                </ul>
              </>
            )}

            <hr />
            <h3>Health Literacy</h3>
            {selectedTip && (
              <>
                <h4>{selectedTip.title}</h4>

                <b>Do’s</b>
                <ul>{selectedTip.dos.map((d,i)=><li key={i}>{d}</li>)}</ul>

                <b>Don’ts</b>
                <ul>{selectedTip.donts.map((d,i)=><li key={i}>{d}</li>)}</ul>

                <b>Seek help if</b>
                <ul>{selectedTip.seek_help.map((d,i)=><li key={i}>{d}</li>)}</ul>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}
