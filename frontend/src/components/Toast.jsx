import { useToast } from '../context/ToastContext'
import { HiCheckCircle, HiExclamationCircle, HiInformationCircle, HiX } from 'react-icons/hi'

const ICONS = {
  success: <HiCheckCircle size={20} />,
  error:   <HiExclamationCircle size={20} />,
  info:    <HiInformationCircle size={20} />,
}

export default function Toast() {
  const { toasts, removeToast } = useToast()

  if (toasts.length === 0) return null

  return (
    <div className="toast-container">
      {toasts.map(toast => (
        <div key={toast.id} className={`toast toast-${toast.type}`}>
          {ICONS[toast.type] || ICONS.info}
          <span>{toast.message}</span>
          <button className="toast-close" onClick={() => removeToast(toast.id)}>
            <HiX />
          </button>
        </div>
      ))}
    </div>
  )
}
