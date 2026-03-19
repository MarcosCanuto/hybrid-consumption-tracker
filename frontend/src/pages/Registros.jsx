import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const CORES= {
  eletrico: {barra: 'bg-blue-500', badge: 'text-blue-600', fundo: 'bg-blue-50'},
  combustao: {barra: 'bg-orange-500', badge: 'text-orange-600', fundo: 'bg-orange-50'},
  checkpoint: {barra: 'bg-gray-400', badge: 'text-gray-500', fundo: 'bg-gray-50'}
}

const TANQUE_TIPOS = {
  1: 'eletrico',
  2: 'combustao'
}

const TANQUE_LABELS = {
  1: 'Abastecimento Elétrico',
  2: 'Abastecimento Combustível'
}

const TANQUE_UNIDADES = {
  1: 'kWh',
  2: 'L'
}

function CardAbastecimento({ registro }) {
  const tipo = registro.tipo === 'checkpoint' ? 'checkpoint' : TANQUE_TIPOS[registro.id_tanque] || 'checkpoint'
  const cores = CORES[tipo]

  return (
    <div className={`relative rounded-xl shadow-sm border border-gray-200 overflow-hidden ${cores.fundo}`}>
      <div className={`absolute left-0 top-0 bottom-0 w-1 ${cores.barra}`} />
      <div className="pl-5 pr-4 py-3">
        <div className="flex justify-between items-start">
          <div>
            <span className={`text-xs font-semibold uppercase tracking-wide ${cores.badge}`}>
              {registro.tipo === 'checkpoint' ? 'Checkpoint' : TANQUE_LABELS[registro.id_tanque]}
            </span>
            <p className="text-xs text-gray-400 mt-0.5">
              {new Date(registro.data).toLocaleString('pt-BR')}
            </p>
          </div>
          <span className="text-sm font-medium text-gray-600">{registro.odometro} km</span>
        </div>

        {registro.quantidade && (
          <p className="mt-2 text-sm text-gray-700">
            {registro.quantidade} <span className="text-gray-400">{TANQUE_UNIDADES[registro.id_tanque]}</span>
            {registro.valor_total && (
              <span className="ml-3 text-gray-400">
                R$ {Number(registro.valor_total).toFixed(2)}
              </span>
            )}
          </p>
        )}

        {registro.observacao && (
          <p className="mt-1 text-xs text-gray-400 italic">{registro.observacao}</p>
        )}
      </div>
    </div>
  )
}

function BarraConfianca({ nivel }) {
  const cor = nivel === 100 ? 'bg-green-500' : nivel >= 85 ? 'bg-orange-500' : nivel >= 70 ? 'bg-yellow-400' : 'bg-red-400'
  const label = nivel === 100 ? 'Alta' : nivel >= 85 ? 'Satisfatória' : nivel >= 70 ? 'Média' : 'Baixa'
  const textoCor = nivel === 100 ? 'text-green-600' : nivel >= 85 ? 'text-orange-600' : nivel >= 70 ? 'text-yellow-600' : 'text-red-500'

  return(
    <div className="flex items-center gap-2 mt-1">
      <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
        <div className={`h-full ${cor} rounded-full` } style={{ width: `${nivel}%` }} />
      </div>
      <span className={`text-xs font-medium ${textoCor}`}>{label}</span>
    </div>
  )
}

function CardTrecho({ consumo }) {
  const hasEletrico = consumo.consumo_eletrico !== null
  const hasCombustao = consumo.consumo_combustao !== null
  const hasAmbos = hasEletrico && hasCombustao

  return (
    <div className="rounded-x1 shadow-sm border border-gray-200 bg-white px-4 py-3">
      <div className="flex justify-between items-center mb-2 ">
        <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">Trecho percorrido</span>
        <span className="text-sm font-medium text-gray-600">{consumo.km_percorridos} km</span>
      </div>

      <div className="flex gap-4">
        {hasEletrico && (
          <div className="flex-1">
            <p className="text-xs font-medium text-blue-500">Elétrico</p>
            <p className="text-base font-bold text-gray-800">
              {Number(consumo.consumo_eletrico).toFixed(2)}
              <span className="text-xs font-normal text-gray-400 ml-1"> km/kWh</span>
            </p>
          </div>
        )}
        {hasCombustao && (
          <div className="flex-1">
            <p className="text-xs font-medium text-orange-500">Combustão</p>
            <p className="text-base font-bold text-gray-800">
              {Number(consumo.consumo_combustao).toFixed(2)}
              <span className="text-xs font-normal text-gray-400 ml-1"> km/L</span>
            </p>
          </div>
        )}
        {hasAmbos && (
        <div className="flex-1">
          <p className="text-xs text-purple-500 font-medium">Híbrido</p>
        </div>
        )}
      </div>

      <BarraConfianca nivel={consumo.nivel_confianca} />
    </div>
  )
}

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

// Monta lista de registros: Se o registro possuir consumo associado, exibe card de trecho.

  function montarTimeline() {
    const timeline = []
    const registrosOrdenados = [...registros]

    for (const registro of registrosOrdenados) {
      const consumo = consumos.find(c => c.id_registro_origem === registro.id)
      if (consumo) {
        timeline.push({ tipo: 'trecho', data: consumo, key: `trecho-${consumo.id}` })
      }
      timeline.push({ tipo: 'registro', data: registro, key: `registro-${registro.id}` })
    }
    return timeline
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-500">Carregando...</p>
      </div>
    )
  }

  {/*
  function buscarConsumo(registroId) {
    return consumos.find(c => c.id_registro_origem === registroId)
  }
  
  function formatarData(data) {
    return new Date(data).toLocaleString('pt-BR')
  }
  */}
  const timeline = montarTimeline()

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">MédiaReal</h1>
        <button
          onClick={() => {
            const odometroAnterior = registros.length > 0 ? registros[0].odometro : '';
            navigate('/registros/novo', { state: { odometroAnterior: odometroAnterior } })
          }}
          className="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + Novo registro
        </button>
      </div>

      {timeline.length === 0 ? (
        <p className="text-gray-400 text-sm text-center mt-16">Nenhum registro encontrado.</p>
      ) : (
        <div className="flex flex-col gap-4">
          {timeline.map(item =>
            item.tipo === 'trecho'
            ? <CardTrecho key={item.key} consumo={item.data} />
            : <CardAbastecimento key={item.key} registro={item.data} />
          )}
        </div>
      )}
    </div>
  )
}