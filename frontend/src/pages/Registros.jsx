import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function Registros() {
  const [registros, setRegistros] = useState([])
  const [consumos, setConsumos] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const ID_VEICULO = 1

  useEffect(() => {
    buscarDados()
  }, [])

  async function buscarDados() {
    try {
      const [resRegistros, resConsumos] = await Promise.all([
        api.get(`/registros/veiculo/${ID_VEICULO}`),
        api.get(`/consumos/veiculo/${ID_VEICULO}`)
      ])
      setRegistros(resRegistros.data.reverse())
      setConsumos(resConsumos.data)
    } catch (error) {
      console.error('Erro ao buscar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  function buscarConsumo(registroId) {
    return consumos.find(c => c.id_registro_origem === registroId)
  }

  function formatarData(data) {
    return new Date(data).toLocaleString('pt-BR')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-500">Carregando...</p>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">MédiaReal</h1>
        <button
          onClick={() => navigate('/registros/novo')}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + Novo registro
        </button>
      </div>

      {registros.length === 0 ? (
        <p className="text-gray-500 text-center mt-10">Nenhum registro encontrado.</p>
      ) : (
        <div className="flex flex-col gap-4">
          {registros.map(registro => {
            const consumo = buscarConsumo(registro.id)
            return (
              <div key={registro.id} className="border rounded-lg p-4 bg-white shadow-sm">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-sm font-medium uppercase text-gray-500">
                      {registro.tipo}
                    </span>
                    <p className="text-sm text-gray-400">{formatarData(registro.data)}</p>
                  </div>
                  <span className="text-sm text-gray-500">
                    {registro.odometro} km
                  </span>
                </div>

                {registro.quantidade && (
                  <p className="mt-2 text-sm">
                    Quantidade: <strong>{registro.quantidade}</strong> {registro.id_tanque === 1 ? 'kWh' : 'L'}
                  </p>
                )}

                {consumo && (
                  <div className="mt-3 pt-3 border-t">
                    <p className="text-sm font-medium text-gray-600">Consumo do trecho anterior</p>
                    <p className="text-sm">km percorridos: <strong>{consumo.km_percorridos}</strong></p>
                    {consumo.consumo_eletrico && (
                      <p className="text-sm">Elétrico: <strong>{Number(consumo.consumo_eletrico).toFixed(2)} km/kWh</strong></p>
                    )}
                    {consumo.consumo_combustao && (
                      <p className="text-sm">Combustão: <strong>{Number(consumo.consumo_combustao).toFixed(2)} km/L</strong></p>
                    )}
                    <p className="text-sm">
                      Confiança: <strong className={consumo.nivel_confianca === 100 ? 'text-green-600' : 'text-yellow-600'}>
                        {consumo.nivel_confianca}%
                      </strong>
                    </p>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}