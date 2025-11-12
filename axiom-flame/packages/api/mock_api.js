const express = require('express');
const app = express();
const port = 8080;

app.use(express.json());

// Root endpoint
app.get('/', (req, res) => {
    res.send('Axiom-Flame Mock API - Ready for Testing');
});

// Health endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        time: new Date().toISOString(),
        message: 'Axiom-Flame API is healthy'
    });
});

// Reason endpoint
app.post('/reason', (req, res) => {
    const { actor, realm, capsule, intent, seal, input } = req.body;
    const dispatchId = `AXF-${new Date().toISOString().slice(0, 10)}-${Math.random().toString(36).substr(2, 8)}`;
    
    res.json({
        ok: true,
        dispatch_id: dispatchId,
        summary: `${intent || 'Reasoning'} sealed for realm ${realm || 'Unknown'}.`,
        actor: actor || 'Custodian',
        realm: realm || 'Unspecified',
        capsule: capsule || 'General',
        timestamp: new Date().toISOString()
    });
});

// Replay endpoint
app.post('/replay', (req, res) => {
    const { dispatch_id } = req.body;
    
    if (!dispatch_id) {
        return res.status(400).json({
            ok: false,
            error: 'dispatch_id required'
        });
    }
    
    res.json({
        ok: true,
        replay: {
            replay_id: `RP-${Math.random().toString(36).substr(2, 8)}`,
            timestamp: new Date().toISOString(),
            source_dispatch_id: dispatch_id,
            realm: 'Test-Realm',
            capsule: 'Test-Capsule',
            audit: {
                status: 'Verified',
                notes: 'Replay authorization matched Eternal Seal'
            }
        }
    });
});

// Audit endpoint
app.post('/audit', (req, res) => {
    const { dispatch_id } = req.body;
    
    if (!dispatch_id) {
        return res.status(400).json({
            ok: false,
            error: 'dispatch_id required'
        });
    }
    
    res.json({
        ok: true,
        dispatch_id,
        audit: 'Present in ledger'
    });
});

app.listen(port, '127.0.0.1', () => {
    console.log(`🚀 Axiom-Flame Mock API running on http://127.0.0.1:${port}`);
    console.log(`📋 Available endpoints:`);
    console.log(`   GET  /health  - Health check`);
    console.log(`   POST /reason  - Dispatch ceremony`);
    console.log(`   POST /replay  - Authorize replay`);
    console.log(`   POST /audit   - Audit ledger`);
});