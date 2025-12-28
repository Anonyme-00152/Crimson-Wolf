# ============================================================
#  Author      : Anonyme-001
#  Project     : Multi-Tool (Educational Purpose Only)
#  Year        : 2025
#
#  DISCLAIMER:
#  This code is provided for EDUCATIONAL PURPOSES ONLY.
#  It is intended to help understand programming, security
#  concepts, and defensive techniques.
#
#  ❌ Any malicious use is strictly prohibited.
#  ❌ Do NOT modify this code to perform illegal actions.
#  ❌ The author is NOT responsible for any misuse.
#
#  By using this code, you agree to use it responsibly
#  and within legal boundaries.
#
#  Copyright (c) 2025 Anonyme-001
#  See LICENSE file for details.
# ============================================================

# Advanced Database Search Engine Pro by Colin

from Plugins.Utils import *
from Plugins.Config import *

try:
    import os
    import re
    import json
    import pickle
    import hashlib
    import mmap
    import time
    import threading
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
    from datetime import datetime
    from pathlib import Path
    import sqlite3
    import pandas as pd
    import csv
    from typing import List, Dict, Tuple, Optional, Set
    import gc
except Exception as e:
    MissingModule(e)

Title("Database Search Engine Pro")
Connection()

class FileIndexer:
    """Advanced file indexing for fast search operations"""
    
    def __init__(self, database_path="Database"):
        self.database_path = Path(database_path).absolute()
        self.index_path = Path("Programs/Extras/search_index")
        self.index_file = self.index_path / "search_index.json"
        self.file_metadata = self.index_path / "file_metadata.json"
        self.index = {}
        self.metadata = {}
        self.lock = threading.Lock()
        
        # Ensure directories exist
        self.database_path.mkdir(parents=True, exist_ok=True)
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing index
        self.load_index()
    
    def load_index(self):
        """Load search index from disk"""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
                print(f"{SUCCESS} Loaded index with {len(self.index)} files", reset)
            
            if self.file_metadata.exists():
                with open(self.file_metadata, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
        except Exception as e:
            print(f"{PREFIX} Could not load index: {e}", reset)
            self.index = {}
            self.metadata = {}
    
    def save_index(self):
        """Save search index to disk"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
            
            with open(self.file_metadata, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            
            print(f"{SUCCESS} Index saved with {len(self.index)} files", reset)
        except Exception as e:
            print(f"{ERROR} Failed to save index: {e}", reset)
    
    def index_file(self, file_path: Path) -> Dict:
        """Index a single file"""
        try:
            file_stat = file_path.stat()
            file_hash = self.calculate_file_hash(file_path)
            
            # Read and index content
            content = self.read_file_content(file_path)
            
            # Create word index
            words = self.extract_words(content)
            word_positions = self.create_word_positions(content, words)
            
            file_info = {
                'path': str(file_path.relative_to(self.database_path)),
                'size': file_stat.st_size,
                'modified': file_stat.st_mtime,
                'hash': file_hash,
                'word_count': len(words),
                'unique_words': len(set(words)),
                'word_positions': word_positions,
                'lines': content.count('\n') + 1
            }
            
            # Add to metadata
            self.metadata[str(file_path.relative_to(self.database_path))] = {
                'size': file_stat.st_size,
                'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'hash': file_hash,
                'indexed_at': datetime.now().isoformat()
            }
            
            return file_info
            
        except Exception as e:
            print(f"{PREFIX} Failed to index {file_path.name}: {e}", reset)
            return None
    
    def index_database(self, force_reindex=False):
        """Index entire database"""
        print(f"{LOADING} Indexing database...", reset)
        
        files_to_index = []
        for file_path in self.database_path.rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(self.database_path))
                
                # Check if needs reindexing
                if not force_reindex and rel_path in self.index:
                    file_stat = file_path.stat()
                    existing_mtime = self.metadata.get(rel_path, {}).get('modified')
                    
                    if existing_mtime and datetime.fromisoformat(existing_mtime).timestamp() >= file_stat.st_mtime:
                        continue
                
                files_to_index.append(file_path)
        
        print(f"{INFO} Found {len(files_to_index)} files to index", reset)
        
        # Index files in parallel
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(self.index_file, file_path): file_path 
                      for file_path in files_to_index[:1000]}  # Limit for performance
            
            completed = 0
            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    file_info = future.result()
                    if file_info:
                        with self.lock:
                            self.index[file_info['path']] = file_info
                        completed += 1
                        
                        if completed % 50 == 0:
                            print(f"{PREFIX} Indexed {completed}/{len(files_to_index)} files", reset)
                except Exception as e:
                    print(f"{PREFIX} Error indexing {file_path.name}: {e}", reset)
        
        self.save_index()
        print(f"{SUCCESS} Indexing complete! {completed} files indexed", reset)
        return completed
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return "0" * 32
    
    def read_file_content(self, file_path: Path) -> str:
        """Read file content with multiple encoding attempts"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # Fallback: read as binary and decode with errors ignored
        try:
            with open(file_path, 'rb') as f:
                return f.read().decode('utf-8', errors='ignore')
        except:
            return ""
    
    def extract_words(self, text: str) -> List[str]:
        """Extract words from text with advanced processing"""
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s@\.\-_#]', ' ', text, flags=re.UNICODE)
        
        # Split into words
        words = re.findall(r'\b[\w@\.\-_]+\b', text, flags=re.UNICODE)
        
        # Filter and normalize
        filtered_words = []
        for word in words:
            word_lower = word.lower()
            # Skip very short words unless they look important
            if len(word) > 2 or (len(word) == 2 and word.isalnum()):
                filtered_words.append(word_lower)
        
        return filtered_words
    
    def create_word_positions(self, content: str, words: List[str]) -> Dict[str, List[int]]:
        """Create index of word positions"""
        word_positions = {}
        content_lower = content.lower()
        
        for word in set(words):
            positions = []
            start = 0
            while True:
                pos = content_lower.find(word, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            if positions:
                word_positions[word] = positions
        
        return word_positions
    
    def search_index(self, search_term: str, case_sensitive=False) -> List[Dict]:
        """Search indexed files for term"""
        results = []
        search_term_lower = search_term.lower() if not case_sensitive else search_term
        
        print(f"{LOADING} Searching index for '{search_term}'...", reset)
        
        for file_path, file_info in self.index.items():
            matches = []
            
            # Check word positions
            for word, positions in file_info.get('word_positions', {}).items():
                if (case_sensitive and search_term in word) or \
                   (not case_sensitive and search_term_lower in word):
                    
                    # Get context around matches
                    for pos in positions[:10]:  # Limit matches per file
                        match_info = {
                            'position': pos,
                            'word': word,
                            'exact_match': search_term_lower == word.lower()
                        }
                        matches.append(match_info)
            
            if matches:
                results.append({
                    'file': file_path,
                    'matches': matches,
                    'metadata': self.metadata.get(file_path, {})
                })
        
        return results

class AdvancedFileSearcher:
    """Advanced file search with multiple techniques"""
    
    def __init__(self, database_path="Database"):
        self.database_path = Path(database_path).absolute()
        self.indexer = FileIndexer(database_path)
        self.cache = {}
        self.search_history = []
    
    def search_files(self, search_term: str, options: Dict = None) -> Dict:
        """Perform advanced file search"""
        if options is None:
            options = {}
        
        # Default options
        default_options = {
            'case_sensitive': False,
            'whole_word': False,
            'regex': False,
            'file_types': None,
            'max_results': 1000,
            'include_binary': False,
            'search_content': True,
            'search_filenames': True,
            'context_lines': 3
        }
        
        options = {**default_options, **options}
        
        print(f"{LOADING} Starting search for '{search_term}'...", reset)
        
        # Record search
        self.search_history.append({
            'term': search_term,
            'options': options,
            'timestamp': datetime.now().isoformat(),
            'results_count': 0
        })
        
        # Use index if available and appropriate
        if not options['regex'] and not options['case_sensitive']:
            indexed_results = self.indexer.search_index(search_term, options['case_sensitive'])
            if indexed_results:
                return self._process_indexed_results(indexed_results, search_term, options)
        
        # Fallback to file scanning
        return self._scan_files(search_term, options)
    
    def _scan_files(self, search_term: str, options: Dict) -> Dict:
        """Scan files for search term"""
        results = {
            'search_term': search_term,
            'options': options,
            'total_files_scanned': 0,
            'files_with_matches': 0,
            'total_matches': 0,
            'results': [],
            'start_time': datetime.now().isoformat()
        }
        
        file_patterns = options.get('file_types', [])
        if file_patterns:
            file_patterns = [fp if fp.startswith('.') else f'.{fp}' for fp in file_patterns]
        
        files_scanned = 0
        
        # Walk through database directory
        for root, dirs, files in os.walk(self.database_path):
            for file_name in files:
                # Filter by file type
                if file_patterns:
                    file_ext = Path(file_name).suffix.lower()
                    if not any(file_ext == pattern.lower() for pattern in file_patterns):
                        continue
                
                file_path = Path(root) / file_name
                relative_path = file_path.relative_to(self.database_path)
                
                files_scanned += 1
                
                # Search in filename
                filename_matches = []
                if options['search_filenames']:
                    filename_matches = self._search_in_text(
                        file_name, search_term, options, is_filename=True
                    )
                
                # Search in content
                content_matches = []
                if options['search_content']:
                    try:
                        file_content = self._read_file_safe(file_path, options['include_binary'])
                        if file_content:
                            content_matches = self._search_in_text(
                                file_content, search_term, options, 
                                context_lines=options['context_lines']
                            )
                    except Exception as e:
                        if options.get('debug', False):
                            print(f"{PREFIX} Error reading {file_name}: {e}", reset)
                
                if filename_matches or content_matches:
                    results['files_with_matches'] += 1
                    results['total_matches'] += len(filename_matches) + len(content_matches)
                    
                    file_result = {
                        'file': str(relative_path),
                        'filename': file_name,
                        'path': str(file_path),
                        'filename_matches': filename_matches,
                        'content_matches': content_matches,
                        'file_info': self._get_file_info(file_path)
                    }
                    
                    results['results'].append(file_result)
                    
                    # Limit results
                    if len(results['results']) >= options['max_results']:
                        print(f"{INFO} Reached maximum results limit ({options['max_results']})", reset)
                        break
            
            # Update progress
            if files_scanned % 100 == 0:
                print(f"\r{PREFIX} Scanned {files_scanned} files, found {results['files_with_matches']} matches", 
                      end='', flush=True)
        
        results['total_files_scanned'] = files_scanned
        results['end_time'] = datetime.now().isoformat()
        
        print(f"\n{SUCCESS} Search complete!", reset)
        return results
    
    def _search_in_text(self, text: str, search_term: str, options: Dict, 
                       is_filename=False, context_lines=0) -> List[Dict]:
        """Search for term in text with advanced options"""
        matches = []
        
        if not text:
            return matches
        
        # Prepare search pattern
        if options['regex']:
            try:
                flags = 0 if options['case_sensitive'] else re.IGNORECASE
                pattern = re.compile(search_term, flags)
            except re.error:
                return matches  # Invalid regex
        else:
            if options['whole_word']:
                pattern = re.compile(rf'\b{re.escape(search_term)}\b', 
                                   re.IGNORECASE if not options['case_sensitive'] else 0)
            else:
                if options['case_sensitive']:
                    pattern = re.compile(re.escape(search_term))
                else:
                    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        
        # Search in text
        if is_filename:
            # For filename, just check if matches
            match = pattern.search(text)
            if match:
                matches.append({
                    'type': 'filename',
                    'match': match.group(),
                    'position': match.start(),
                    'context': text
                })
        else:
            # For content, get line-by-line matches
            lines = text.split('\n')
            for line_num, line in enumerate(lines, 1):
                line_matches = list(pattern.finditer(line))
                
                for match in line_matches:
                    # Get context
                    start_context = max(0, line_num - context_lines - 1)
                    end_context = min(len(lines), line_num + context_lines)
                    context = '\n'.join(lines[start_context:end_context])
                    
                    matches.append({
                        'type': 'content',
                        'line_number': line_num,
                        'match': match.group(),
                        'position': match.start(),
                        'line': line,
                        'context': context,
                        'highlighted_line': self._highlight_match(line, match)
                    })
        
        return matches
    
    def _highlight_match(self, text: str, match) -> str:
        """Highlight match in text"""
        start = match.start()
        end = match.end()
        highlighted = f"{text[:start]}{red}{text[start:end]}{white}{text[end:]}"
        return highlighted
    
    def _read_file_safe(self, file_path: Path, include_binary=False) -> Optional[str]:
        """Read file safely with multiple encodings"""
        # Check if binary file
        try:
            with open(file_path, 'rb') as f:
                sample = f.read(1024)
                
            # Detect binary files
            textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
            is_binary = bool(sample.translate(None, textchars))
            
            if is_binary and not include_binary:
                return None
        except:
            return None
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16-le', 'utf-16-be']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                    return f.read()
            except (UnicodeDecodeError, LookupError):
                continue
        
        # Fallback: decode with errors ignored
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return content.decode('utf-8', errors='ignore')
        except:
            return None
    
    def _get_file_info(self, file_path: Path) -> Dict:
        """Get file information"""
        try:
            stat = file_path.stat()
            return {
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'is_file': file_path.is_file(),
                'is_dir': file_path.is_dir(),
                'extension': file_path.suffix.lower()
            }
        except:
            return {}
    
    def _process_indexed_results(self, indexed_results, search_term, options):
        """Process results from index"""
        results = {
            'search_term': search_term,
            'options': options,
            'source': 'index',
            'files_with_matches': len(indexed_results),
            'total_matches': sum(len(r['matches']) for r in indexed_results),
            'results': []
        }
        
        for indexed_result in indexed_results:
            file_result = {
                'file': indexed_result['file'],
                'filename': Path(indexed_result['file']).name,
                'metadata': indexed_result['metadata'],
                'content_matches': []
            }
            
            # Convert index matches to content matches
            for match in indexed_result['matches']:
                file_result['content_matches'].append({
                    'type': 'content',
                    'match': match['word'],
                    'position': match['position'],
                    'exact_match': match['exact_match']
                })
            
            results['results'].append(file_result)
        
        return results

class SearchResultsRenderer:
    """Render search results in beautiful format"""
    
    @staticmethod
    def display_results(search_results: Dict):
        """Display search results"""
        if not search_results.get('results'):
            Scroll(f"""
 {ERROR} No results found for '{search_results.get('search_term', '')}'
 {PREFIX} Files scanned: {red}{search_results.get('total_files_scanned', 0)}{white}
""")
            return
        
        header = f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               SEARCH RESULTS REPORT                     ║
{red}╚══════════════════════════════════════════════════════════╝{reset}
"""
        
        stats = f"""
 {PREFIX1}📊 SEARCH STATISTICS{SUFFIX1}
 {SUCCESS} Search Term  :{red} {search_results.get('search_term', 'N/A')}
 {SUCCESS} Files Scanned:{red} {search_results.get('total_files_scanned', 0):,}
 {SUCCESS} Files Found  :{red} {search_results.get('files_with_matches', 0):,}
 {SUCCESS} Total Matches:{red} {search_results.get('total_matches', 0):,}
 {SUCCESS} Search Source:{red} {search_results.get('source', 'file_scan')}
 {SUCCESS} Search Time  :{red} {search_results.get('start_time', 'N/A')}
"""
        
        Scroll(header + stats)
        
        # Display each result
        for i, result in enumerate(search_results['results'][:50], 1):  # Limit to 50 results
            print(f"\n{PREFIX1}{i:03d}{SUFFIX1} {red}{result['file']}{white}")
            print(f" {SUCCESS}File:{red} {result['filename']}{white}")
            
            if 'file_info' in result:
                size_mb = result['file_info'].get('size', 0) / (1024 * 1024)
                print(f" {SUCCESS}Size:{red} {size_mb:.2f} MB{white}")
                print(f" {SUCCESS}Modified:{red} {result['file_info'].get('modified', 'N/A')}{white}")
            
            # Display filename matches
            if result.get('filename_matches'):
                print(f" {SUCCESS}Filename Matches:{white}")
                for match in result['filename_matches'][:3]:  # Limit matches
                    print(f"   {PREFIX}»{white} {match.get('context', '')}")
            
            # Display content matches
            if result.get('content_matches'):
                print(f" {SUCCESS}Content Matches:{white}")
                for match in result['content_matches'][:5]:  # Limit matches
                    if 'line_number' in match:
                        print(f"   {PREFIX}Line {match['line_number']}:{white} {match.get('highlighted_line', match.get('line', ''))}")
                    elif 'match' in match:
                        print(f"   {PREFIX}»{white} Found: {red}{match['match']}{white}")
            
            print()
            
            # Pagination
            if i % 10 == 0 and i < len(search_results['results']):
                input(f"{INPUT} Press Enter for more results {red}->{reset} ")
                Clear()
                print(header)
        
        # Summary
        print(f"\n{PREFIX} {INFO} Displayed {min(50, len(search_results['results']))} of {len(search_results['results'])} results", reset)
    
    @staticmethod
    def save_results(search_results: Dict, format='json'):
        """Save search results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        search_term = search_results.get('search_term', 'search').replace('/', '_')
        filename = f"search_results_{search_term}_{timestamp}"
        
        try:
            if format == 'json':
                filename += '.json'
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(search_results, f, indent=2, ensure_ascii=False, default=str)
            
            elif format == 'csv':
                filename += '.csv'
                # Flatten results for CSV
                rows = []
                for result in search_results['results']:
                    row = {
                        'file': result['file'],
                        'filename': result['filename'],
                        'filename_matches': len(result.get('filename_matches', [])),
                        'content_matches': len(result.get('content_matches', [])),
                        'total_matches': len(result.get('filename_matches', [])) + len(result.get('content_matches', []))
                    }
                    if 'file_info' in result:
                        row.update(result['file_info'])
                    rows.append(row)
                
                if rows:
                    df = pd.DataFrame(rows)
                    df.to_csv(filename, index=False, encoding='utf-8')
            
            elif format == 'txt':
                filename += '.txt'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Search Results Report\n")
                    f.write(f"Search Term: {search_results.get('search_term')}\n")
                    f.write(f"Total Files: {search_results.get('total_files_scanned')}\n")
                    f.write(f"Files with Matches: {search_results.get('files_with_matches')}\n")
                    f.write(f"Total Matches: {search_results.get('total_matches')}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for result in search_results['results']:
                        f.write(f"File: {result['file']}\n")
                        f.write(f"Matches: {len(result.get('content_matches', []))}\n")
                        
                        for match in result.get('content_matches', [])[:3]:
                            if 'line_number' in match:
                                f.write(f"  Line {match['line_number']}: {match.get('line', '')}\n")
                        
                        f.write("\n")
            
            print(f"{SUCCESS} Results saved to {red}{filename}{white}", reset)
            return filename
            
        except Exception as e:
            print(f"{ERROR} Failed to save results: {e}", reset)
            return None

def advanced_search_mode():
    """Advanced search interface"""
    searcher = AdvancedFileSearcher()
    
    while True:
        Clear()
        Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               ADVANCED SEARCH ENGINE                    ║
{red}╚══════════════════════════════════════════════════════════╝{reset}

 {PREFIX1}1{SUFFIX1} Quick Search
 {PREFIX1}2{SUFFIX1} Advanced Search with Options
 {PREFIX1}3{SUFFIX1} Rebuild Search Index
 {PREFIX1}4{SUFFIX1} View Search History
 {PREFIX1}5{SUFFIX1} Return to Menu

""")
        
        choice = input(f"{INPUT} Select option {red}->{reset} ").strip()
        
        if choice == '1':
            search_term = input(f"{INPUT} Search term {red}->{reset} ").strip()
            if search_term:
                results = searcher.search_files(search_term)
                SearchResultsRenderer.display_results(results)
                
                # Offer to save results
                print(f"\n{PREFIX} Save results? (y/n): ", end='')
                if input().strip().lower() == 'y':
                    print(f"{PREFIX} Select format: {red}1{white}. JSON, {red}2{white}. CSV, {red}3{white}. TXT")
                    format_choice = input(f"{INPUT} Format {red}->{reset} ").strip()
                    formats = {'1': 'json', '2': 'csv', '3': 'txt'}
                    format_selected = formats.get(format_choice, 'json')
                    SearchResultsRenderer.save_results(results, format_selected)
                
                Continue()
        
        elif choice == '2':
            search_term = input(f"{INPUT} Search term {red}->{reset} ").strip()
            
            if search_term:
                print(f"\n{PREFIX} Advanced Options:", reset)
                
                options = {}
                
                print(f" {PREFIX1}1{SUFFIX1} Case Sensitive: {red}{'Yes' if input(f'{INPUT} Case sensitive? (y/n) {red}->{reset} ').lower() == 'y' else 'No'}{white}")
                if input(f"{INPUT} Whole word only? (y/n) {red}->{reset} ").lower() == 'y':
                    options['whole_word'] = True
                
                if input(f"{INPUT} Use regex? (y/n) {red}->{reset} ").lower() == 'y':
                    options['regex'] = True
                
                print(f"{PREFIX} File types to search (comma separated, leave empty for all):", reset)
                file_types = input(f"{INPUT} File types {red}->{reset} ").strip()
                if file_types:
                    options['file_types'] = [ft.strip() for ft in file_types.split(',')]
                
                try:
                    max_results = int(input(f"{INPUT} Max results (default 1000) {red}->{reset} ") or "1000")
                    options['max_results'] = max_results
                except:
                    options['max_results'] = 1000
                
                try:
                    context_lines = int(input(f"{INPUT} Context lines (default 3) {red}->{reset} ") or "3")
                    options['context_lines'] = context_lines
                except:
                    options['context_lines'] = 3
                
                results = searcher.search_files(search_term, options)
                SearchResultsRenderer.display_results(results)
                
                # Offer to save results
                print(f"\n{PREFIX} Save results? (y/n): ", end='')
                if input().strip().lower() == 'y':
                    SearchResultsRenderer.save_results(results)
                
                Continue()
        
        elif choice == '3':
            print(f"{LOADING} Rebuilding search index...", reset)
            force = input(f"{INPUT} Force reindex all files? (y/n) {red}->{reset} ").lower() == 'y'
            count = searcher.indexer.index_database(force_reindex=force)
            print(f"{SUCCESS} Index rebuilt with {count} files", reset)
            Continue()
        
        elif choice == '4':
            if searcher.search_history:
                Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║                 SEARCH HISTORY                          ║
{red}╚══════════════════════════════════════════════════════════╝{reset}
""")
                for i, history in enumerate(reversed(searcher.search_history[-20:]), 1):
                    timestamp = datetime.fromisoformat(history['timestamp']).strftime("%Y-%m-%d %H:%M")
                    print(f" {PREFIX1}{i:02d}{SUFFIX1} {timestamp} | {red}{history['term']}{white}")
                    print(f"      {SUCCESS}Results:{red} {history.get('results_count', 0)}{white}")
                    print()
            else:
                print(f"{INFO} No search history available", reset)
            Continue()
        
        elif choice == '5':
            break
        
        else:
            ErrorChoice()

try:
    advanced_search_mode()
    Continue()
    Reset()

except KeyboardInterrupt:
    print(f"\n{PREFIX} {INFO} Operation cancelled by user", reset)
    Continue()
    Reset()
except Exception as e:
    Error(e)