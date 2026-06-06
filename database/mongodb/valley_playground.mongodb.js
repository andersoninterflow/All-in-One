/* global use, db */
// MongoDB Playground for Valley Project
// Crie ou selecione o banco de dados do projeto.
const database = 'valley_db';
const collectionAiMemory = 'ai_memory';
const collectionSocialVideos = 'social_videos';
const collectionInfluencerMetrics = 'influencer_metrics';
const collectionTelemetryLogs = 'telemetry_logs';

use(database);

db.getCollection(collectionAiMemory).insertMany([
  { user_id: 'user-123', context: 'preferencias_mobilidade', memory_data: { prefere_silencio: true, temperatura: 22 }, created_at: new Date(), updated_at: new Date() },
  { user_id: 'user-456', context: 'historico_compras', memory_data: { categorias_favoritas: ['eletronicos', 'livros'] }, created_at: new Date(), updated_at: new Date() }
]);

console.log('--- AI Memory ---');
console.log(db.getCollection(collectionAiMemory).find({ user_id: 'user-123' }).toArray());
