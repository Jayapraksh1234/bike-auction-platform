import React, { useEffect, useMemo, useState } from 'react';

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

function money(value) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(Number(value || 0));
}
function timeLeft(endTime) {
  const diff = new Date(endTime).getTime() - Date.now();
  if (diff <= 0) return 'Auction ended';
  const hours = Math.floor(diff / 3600000);
  const mins = Math.floor((diff % 3600000) / 60000);
  const days = Math.floor(hours / 24);
  return days ? `${days}d ${hours % 24}h left` : hours ? `${hours}h ${mins}m left` : `${mins}m left`;
}

export default function App() {
  const [auctions, setAuctions] = useState([]);
  const [selected, setSelected] = useState(null);
  const [bids, setBids] = useState([]);
  const [filter, setFilter] = useState('all');
  const [token, setToken] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [bidAmount, setBidAmount] = useState('');
  const [notice, setNotice] = useState('');
  const [busy, setBusy] = useState(false);

  const headers = useMemo(() => token ? { Authorization: `Bearer ${token}` } : {}, [token]);

  async function loadAuctions() {
    try {
      const res = await fetch(`${API}/auctions/`);
      if (!res.ok) throw new Error('Could not load auctions.');
      setAuctions(await res.json());
    } catch (e) { setNotice(e.message); }
  }
  async function loadBids(auctionId) {
    try {
      const res = await fetch(`${API}/auctions/${auctionId}/bids/`);
      if (res.ok) setBids(await res.json());
    } catch { /* Keep the current list visible if a refresh fails. */ }
  }
  async function openAuction(auction) {
    setSelected(auction);
    setBidAmount(String(auction.minimum_next_bid));
    await loadBids(auction.id);
  }
  useEffect(() => { loadAuctions(); const id = setInterval(loadAuctions, 15000); return () => clearInterval(id); }, []);
  useEffect(() => {
    if (!selected) return;
    const id = setInterval(async () => {
      await loadAuctions();
      await loadBids(selected.id);
      const response = await fetch(`${API}/auctions/${selected.id}/`);
      if (response.ok) setSelected(await response.json());
    }, 5000);
    return () => clearInterval(id);
  }, [selected?.id]);

  async function login(event) {
    event.preventDefault(); setNotice(''); setBusy(true);
    try {
      const res = await fetch(`${API}/auth/token/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Login failed. Check your credentials.');
      setToken(data.access); setNotice(`Signed in as ${username}.`);
    } catch (e) { setNotice(e.message); }
    finally { setBusy(false); }
  }
  async function placeBid(event) {
    event.preventDefault();
    if (!selected) return;
    setBusy(true); setNotice('');
    try {
      const res = await fetch(`${API}/auctions/${selected.id}/bid/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...headers },
        body: JSON.stringify({ amount: bidAmount })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || data.amount || 'Bid rejected. Refresh and try again.');
      setNotice(`Bid submitted: ${money(data.amount)}.`);
      await loadAuctions();
      await loadBids(selected.id);
      const latest = await fetch(`${API}/auctions/${selected.id}/`);
      if (latest.ok) setSelected(await latest.json());
    } catch (e) { setNotice(typeof e.message === 'string' ? e.message : 'Bid rejected.'); }
    finally { setBusy(false); }
  }

  const shown = auctions.filter(a => filter === 'all' || a.status === filter);
  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="#" onClick={e => { e.preventDefault(); setSelected(null); }}><span className="brand-mark">R</span><span>RevBid<span className="brand-dot">.</span></span></a>
      <nav><a href="#auctions" onClick={() => setSelected(null)}>Auctions</a><a href="#how">How it works</a></nav>
      <div className="user-area">
        {token ? <span className="signed-in">● {username}</span> : <form className="login-form" onSubmit={login}>
          <input aria-label="Username" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
          <input aria-label="Password" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          <button className="btn btn-dark" disabled={busy}>Sign in</button>
        </form>}
      </div>
    </header>

    <main>
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow"><span className="pulse"></span> THE NEXT RIDE IS YOURS</div>
          <h1>Find your ride.<br /><em>Win the road.</em></h1>
          <p>A better way to discover pre-owned motorcycles. Transparent bidding, real-time prices, and your next story waiting to start.</p>
          <a className="btn btn-lime" href="#auctions">Explore live auctions <span>↗</span></a>
          <div className="hero-stats"><div><strong>{auctions.length.toString().padStart(2, '0')}</strong><span>Listed auctions</span></div><div><strong>100%</strong><span>Bid transparency</span></div><div><strong>₹</strong><span>Secure bidding</span></div></div>
        </div>
        <div className="hero-art">
          <div className="art-glow"></div>
          <div className="art-tag">BUILT FOR THE RIDE <span>✳</span></div>
          <img src="https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=1200&q=85" alt="Motorcycle on a road" />
          <div className="art-caption"><span>THE OPEN ROAD</span><strong>Your next chapter starts here.</strong></div>
          <div className="art-number">01 / RIDE</div>
        </div>
      </section>

      <section className="auction-section" id="auctions">
        <div className="section-heading"><div><div className="eyebrow">CURATED FOR RIDERS</div><h2>Live <em>auctions.</em></h2></div><div className="filters">
          {['all', 'live', 'scheduled', 'ended'].map(f => <button key={f} className={filter === f ? 'filter active' : 'filter'} onClick={() => setFilter(f)}>{f === 'all' ? 'All bikes' : f[0].toUpperCase() + f.slice(1)}</button>)}
        </div></div>
        {notice && <div className="notice" role="status"><span>{notice}</span><button onClick={() => setNotice('')} aria-label="Dismiss message">×</button></div>}
        {shown.length === 0 ? <div className="empty"><div className="empty-icon">↗</div><h3>No auctions to show just yet</h3><p>Try another filter or check back soon.</p><button className="btn btn-dark" onClick={loadAuctions}>Refresh auctions</button></div> :
          <div className="bike-grid">{shown.map((a, i) => <article className="bike-card" key={a.id}>
            <button className="bike-image" onClick={() => openAuction(a)} aria-label={`View ${a.motorcycle.title}`}>
              {a.motorcycle.image_url ? <img src={a.motorcycle.image_url} alt={a.motorcycle.title} /> : <img src={`https://images.unsplash.com/photo-${['1558981806-ec527fa84c39','1558981403-c5f9899a28bc','1568772585407-9361f9bf3a87'][i % 3]}?auto=format&fit=crop&w=800&q=80`} alt={a.motorcycle.title} />}
              <span className={`status status-${a.status}`}>{a.status === 'live' && <i></i>}{a.status}</span><span className="card-arrow">↗</span>
            </button>
            <div className="bike-info"><div className="bike-meta"><span>{a.motorcycle.year}</span><span>·</span><span>{a.motorcycle.mileage_km.toLocaleString('en-IN')} km</span></div><h3>{a.motorcycle.title}</h3><p className="bike-description">{a.motorcycle.description}</p>
              <div className="price-row"><div><span className="small-label">{a.status === 'scheduled' ? 'STARTING PRICE' : 'CURRENT BID'}</span><strong>{money(a.current_price)}</strong></div><div className="time-left">{timeLeft(a.end_time)}</div></div>
              <button className="card-cta" onClick={() => openAuction(a)}>View auction <span>→</span></button>
            </div>
          </article>)}</div>}
      </section>

      <section className="how-section" id="how"><div><div className="eyebrow">SIMPLE BY DESIGN</div><h2>Three steps.<br /><em>One great ride.</em></h2></div>
        <div className="steps"><div><span>01</span><h3>Discover</h3><p>Browse used motorcycles and explore each listing's details.</p></div><div><span>02</span><h3>Place your bid</h3><p>Sign in and make a bid that meets the minimum required amount.</p></div><div><span>03</span><h3>Ride into your next chapter</h3><p>Follow the auction status and see the latest bidding activity.</p></div></div>
      </section>
    </main>
    {selected && <div className="modal-backdrop" role="presentation" onMouseDown={e => { if (e.target === e.currentTarget) setSelected(null); }}>
      <section className="auction-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <button className="modal-close" onClick={() => setSelected(null)} aria-label="Close auction">×</button>
        <div className="modal-photo">{selected.motorcycle.image_url ? <img src={selected.motorcycle.image_url} alt="" /> : <img src="https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=1200&q=85" alt="" />}</div>
        <div className="modal-body"><div className="eyebrow">AUCTION #{selected.id} · {selected.status.toUpperCase()}</div><h2 id="modal-title">{selected.motorcycle.title}</h2><p>{selected.motorcycle.description}</p>
          <div className="detail-grid"><div><span>Current price</span><strong>{money(selected.current_price)}</strong></div><div><span>Minimum next bid</span><strong>{money(selected.minimum_next_bid)}</strong></div><div><span>Year</span><strong>{selected.motorcycle.year}</strong></div><div><span>Mileage</span><strong>{selected.motorcycle.mileage_km.toLocaleString('en-IN')} km</strong></div></div>
          <form className="bid-form" onSubmit={placeBid}><label htmlFor="bid-amount">Your bid (INR)</label><div><input id="bid-amount" type="number" min={selected.minimum_next_bid} step="0.01" value={bidAmount} onChange={e => setBidAmount(e.target.value)} required /><button className="btn btn-dark" disabled={busy || selected.status !== 'live'}>{busy ? 'Please wait…' : 'Place bid ↗'}</button></div>{!token && <small>Sign in above before placing a bid.</small>}</form>
          <div className="bid-history"><h3>Recent bids <span>{bids.length}</span></h3>{bids.length ? bids.slice(0, 8).map(b => <div className="bid-item" key={b.id}><div><strong>{b.bidder_username}</strong><small>{new Date(b.created_at).toLocaleString()}</small></div><strong>{money(b.amount)}</strong></div>) : <p>No bids yet. Be the first to bid.</p>}</div>
        </div>
      </section>
    </div>}
    <footer><a className="brand" href="#"><span className="brand-mark">R</span><span>RevBid<span className="brand-dot">.</span></span></a><span>Built for the love of the ride.</span><span>Demo project · Bidding is not a real purchase</span></footer>
  </div>;
}
