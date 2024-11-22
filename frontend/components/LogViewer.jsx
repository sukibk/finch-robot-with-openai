const LogViewer = ({ logs }) => (
    <div className="p-4 bg-gray-100 border">
        <h3 className="font-bold">Command Logs</h3>
        <ul>
            {logs.map((log, index) => (
                <li key={index}>{log}</li>
            ))}
        </ul>
    </div>
);

export default LogViewer;
